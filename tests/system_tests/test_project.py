import asyncio
import os

import bson
import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import Select


driver: webdriver.Firefox = None


def setup_module(module):
    global driver
    driver = webdriver.Firefox()


def teardown_module(module):
    driver.close()
    os.remove('././geckodriver.log')


@pytest.fixture(autouse=True)
def prepare():
    driver.delete_all_cookies()


async def wait_new_url(old_url):
    i = 0
    while True:
        if i > 100:
            print('timed out')
        elif driver.current_url == old_url:
            await asyncio.sleep(0.01)
            i += 1
            continue
        break


async def sign_in():
    driver.get('http://localhost:8080/sign_in')
    input_login = driver.find_element_by_id('inputLogin')
    input_login.send_keys('sanyash')
    input_password = driver.find_element_by_id('inputPassword')
    input_password.send_keys('nyash_myash')
    input = driver.find_element_by_name('sign_in')
    old_url = driver.current_url
    input.submit()
    await wait_new_url(old_url)


async def sign_out():
    input = driver.find_element_by_name('sign_out')
    old_url = driver.current_url
    input.submit()
    await wait_new_url(old_url)


async def test_main_page():
    driver.get('http://localhost:8080')
    assert driver.title == 'FakeProjectEuler'
    navbar_brand = driver.find_element_by_class_name('navbar-brand')
    assert navbar_brand.text == 'FakeProjectEuler'
    nav_items = driver.find_elements_by_class_name('nav-item')
    assert [nav_item.text for nav_item in nav_items] == [
        'About', 'Archives', 'Statistics', 'Register', 'Sign In'
    ]
    footer = driver.find_element_by_class_name('footer')
    assert footer.text == 'Powered by Shilov Alexandr'


async def test_sign_in():
    await sign_in()
    cookie = driver.get_cookies()[0]
    assert cookie['name'] == 'projecteuler-user-token'
    assert bson.ObjectId.is_valid(cookie['value'])


@pytest.mark.parametrize(
    'query, expected_task_ids',
    [
        (
            '',
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ),
        (
            '?page=5',
            [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        ),
        (
            '?sort_by=difficulty&sort_order=asc',
            [11, 24, 49, 44, 23, 52, 37, 19, 14, 28]
        ),
        (
            '?sort_by=solved_by&sort_order=desc',
            [8, 1, 26, 25, 5, 50, 35, 16, 44, 21]
        ),
        (
            '?solved=yes',
            [1, 3, 6, 8, 12, 13, 14, 16, 19, 22]
        )
    ]
)
async def test_archives(query, expected_task_ids):
    await sign_in()
    driver.get('http://localhost:8080/archives{}'.format(query))
    task_ids = driver.find_elements_by_name('id')
    assert [int(task_id.text) for task_id in task_ids] == expected_task_ids


async def test_sign_out():
    await sign_in()
    assert driver.get_cookies() != []
    driver.get('http://localhost:8080/archives')
    await sign_out()
    assert driver.get_cookies() == []


async def test_task():
    await sign_in()
    driver.get('http://localhost:8080/task?id=1')
    title = driver.find_element_by_tag_name('h1')
    assert title.text == 'Multiples of 3 and 5'
    text = driver.find_element_by_name('text')
    assert text.text == (
        'If we list all the natural numbers below 10 '
        'that are multiples of 3 or 5, we get 3, 5, 6 and 9. '
        'The sum of these multiples is 23.\n'
        'Find the sum of all the multiples of 3 or 5 below 1000.'
    )
    answer = driver.find_element_by_class_name('answer')
    assert answer.text == 'answer: 233168'


async def test_account():
    await sign_in()
    driver.get('http://localhost:8080/account')
    login = driver.find_element_by_name('login')
    assert login.get_attribute('value') == 'sanyash'
    password = driver.find_element_by_name('password')
    assert password.get_attribute('value') == 'nyash_myash'
    email = driver.find_element_by_name('email')
    assert email.get_attribute('value') == 'sasha1998lost@yandex.ru'
    phone = driver.find_element_by_name('phone')
    assert phone.get_attribute('value') == '+79167419038'
    country = Select(driver.find_element_by_name('country'))
    selected = country.first_selected_option.text
    assert selected == 'Russia'
    programming_language = Select(
        driver.find_element_by_name('programming_language')
    )
    selected = programming_language.first_selected_option.text
    assert selected == 'Python'
