from hamcrest import assert_that, equal_to, greater_than, is_, not_none
from selenium import webdriver
from selenium.webdriver.common.by import By
from pytest_bdd import scenario, given, when, then
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import (
    expected_conditions as ExpectedConditions,
)


@scenario(
    "decision_point.feature",
    "Creating a decision point"
)
def test_create_decision_point_with_requests():
    pass


@given("the user is logged in")
def log_user_in(driver: webdriver.Remote, login_user: None):
    sleep(1)
    assert_that(driver.get_cookie("SDSESSION"), is_(not_none()))


@given("the home page is displayed")
def check_is_on_homepage(driver: webdriver.Remote):
    assert_that(driver.current_url.endswith("/app/"), is_(equal_to(True)))


@when("I click on a patient row")
def insert_correct_credentials(driver: webdriver.Remote):
    patient_list = driver.find_elements(By.CLASS_NAME, 'sd-hidden-button')
    assert_that(len(patient_list), is_(greater_than(0)))

    for patient_button in patient_list:
        if patient_button.get_property("disabled") is False or None:
            patient_button.click()
            break


@then("I should see the decision point modal")
def check_modal_present(driver: webdriver.Remote):
    driver.find_element(By.CSS_SELECTOR, '.modal-body')


@given("I fill the text boxes")
def complete_form(driver: webdriver.Remote):
    clinical_history = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.NAME, "clinicHistory")
    )
    clinical_history.send_keys("clinical_history")

    comorbidities = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.NAME, "comorbidities")
    )
    comorbidities.send_keys("comorbidities")


@when("I submit the form")
def submit_form(driver: webdriver.Remote):
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Submit')]"
    ).click()


@then("I should see a confirmation of no requests selected")
def check_no_request_confirmation(driver: webdriver.Remote):
    driver.find_element(
        By.XPATH,
        "//h2[contains(text(), 'No requests selected!')]"
    )


@when("I go back, select a request and resubmit")
def select_requests(driver: webdriver.Remote):
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Cancel')]"
    ).click()

    checkbox = driver.find_elements(By.XPATH, "//input[@type='checkbox']")[0]

    WebDriverWait(driver, 10).until(
        ExpectedConditions.element_to_be_clickable(
            checkbox
        )
    )

    checkbox.click()

    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Submit')]"
    ).click()


@then("I should see a pre-submission confirmation window")
def check_presub_confirmation(driver: webdriver.Remote):
    driver.find_element(
        By.XPATH,
        "//h2[contains(text(), 'Submit these requests')]"
    )


@when("I submit the pre-submission confirmation")
def submit_presub_confirmation(driver: webdriver.Remote):
    driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]").click()


@then("I should see the server confirmation window")
def check_server_confirmation(driver: webdriver.Remote):
    driver.find_element(
        By.XPATH,
        "//h2[contains(text(), 'Decision Submitted')]"
    )


@when("I submit the server confirmation")
def submit_server_confirmation(driver: webdriver.Remote):
    driver.find_element(By.XPATH, "//button[contains(text(), 'OK')]").click()


@then("it should close the modal")
def check_close_modal(driver: webdriver.Remote):
    assert_that(
        len(driver.find_elements(By.CSS_SELECTOR, '.modal-body')),
        equal_to(0)
    )
