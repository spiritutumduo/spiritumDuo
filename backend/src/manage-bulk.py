import asyncio
import sys
from common import DataCreatorInputErrors
from models import (
    Pathway,
    Patient,
    DecisionPoint,
    Milestone,
    MilestoneType,
    User,
    Session,
    OnPathway,
    Role,
    RolePermission, UserRole,
    PathwayMilestoneType,
    UserPathway
)
from containers import SDContainer
from asyncpg.exceptions import UndefinedTableError
from models.db import db, DATABASE_URL
from api import app
from faker import Faker
from random import randint, getrandbits
from datetime import date
from SdTypes import MilestoneState, Permissions
from itsdangerous import TimestampSigner
from trustadapter.trustadapter import (
    Patient_IE,
    TestResult_IE,
    TestResultRequest_IE,
    TestResultRequestImmediately_IE,
    TrustIntegrationCommunicationError,
    PseudoTrustAdapter
)
from config import config
from base64 import b64encode
from typing import Dict, List
from bcrypt import hashpw, gensalt

faker = Faker()
app.container = SDContainer()

NUMBER_OF_USERS_PER_PATHWAY = 10
NUMBER_OF_PATHWAYS = 20
NUMBER_OF_PATIENTS_PER_PATHWAY = 50


class RequestPlaceholder(dict):
    """
    This is a test
    """


_CONTEXT = {
    "db": db,
    "request": RequestPlaceholder()
}

signer = TimestampSigner(config['SESSION_SECRET_KEY'])
random_cookie_value = b64encode(str(getrandbits(64)).encode("utf-8"))
SESSION_COOKIE = signer.sign(random_cookie_value).decode("utf-8")

_CONTEXT['request'].cookies = {
    "SDSESSION": SESSION_COOKIE
}


async def check_connection():
    print("Testing connection...")
    try:
        await PseudoTrustAdapter().test_connection(
            auth_token=_CONTEXT['request'].cookies['SDSESSION']
        )
    except TrustIntegrationCommunicationError as e:
        print(e)
        print("Connection failed!")
        sys.exit(1)
    else:
        print("Connection successful!")


async def clear_existing_data():
    print("Clearing existing data from pseudotie database")
    await PseudoTrustAdapter().clear_database(
        auth_token=_CONTEXT['request'].cookies['SDSESSION']
    )

    print("Clearing existing data from local database")

    try:
        await UserRole.delete.gino.status()
        print("Table `UserRole` deleted")
    except UndefinedTableError:
        print("Table `UserRole` not found. Continuing")

    try:
        await RolePermission.delete.gino.status()
        print("Table `RolePermission` deleted")
    except UndefinedTableError:
        print("Table `RolePermission` not found. Continuing")

    try:
        await Role.delete.gino.status()
        print("Table `Role` deleted")
    except UndefinedTableError:
        print("Table `delete` not found. Continuing")

    try:
        await Milestone.delete.where(Milestone.id >= 0).gino.status()
        print("Table `Milestone` deleted")
    except UndefinedTableError:
        print("Table `Milestone` not found. Continuing")

    try:
        await DecisionPoint.delete.where(DecisionPoint.id >= 0).gino.status()
        print("Table `DecisionPoint` deleted")
    except UndefinedTableError:
        print("Table `DecisionPoint` not found. Continuing")

    try:
        await OnPathway.delete.where(OnPathway.id >= 0).gino.status()
        print("Table `OnPathway` deleted")
    except UndefinedTableError:
        print("Table `OnPathway` not found. Continuing")

    try:
        await Session.delete.gino.status()
        print("Table `Session` deleted")
    except UndefinedTableError:
        print("Table `Session` not found. Continuing")

    try:
        await UserPathway.delete.gino.status()
        print("Table `UserPathway` deleted")
    except UndefinedTableError:
        print("Table `UserPathway` not found. Continuing")

    try:
        await User.delete.where(User.id >= 0).gino.status()
        print("Table `User` deleted")
    except UndefinedTableError:
        print("Table `User` not found. Continuing")

    try:
        await Patient.delete.where(Patient.id >= 0).gino.status()
        print("Table `Patient` deleted")
    except UndefinedTableError:
        print("Table `Patient` not found. Continuing")

    try:
        await PathwayMilestoneType.delete.where(MilestoneType.id >= 0)\
            .gino.status()
        print("Table `PathwayMilestoneType` deleted")
    except UndefinedTableError:
        print("Table `PathwayMilestoneType` not found. Continuing")

    try:
        await Pathway.delete.where(Pathway.id >= 0).gino.status()
        print("Table `Pathway` deleted")
    except UndefinedTableError:
        print("Table `Pathway` not found. Continuing")

    try:
        await MilestoneType.delete.where(MilestoneType.id >= 0).gino.status()
        print("Table `MilestoneType` deleted")
    except UndefinedTableError:
        print("Table `MilestoneType` not found. Continuing")


async def create_roles():
    doctor_role = await Role.create(
        name="GP"
    )
    admin_role = await Role.create(
        name="admin"
    )
    for perm in Permissions:
        if (perm is not Permissions.USER_CREATE)\
                and (perm is not Permissions.USER_UPDATE)\
                and (perm is not Permissions.ROLE_CREATE)\
                and (perm is not Permissions.ROLE_UPDATE)\
                and (perm is not Permissions.ROLE_DELETE)\
                and (perm is not Permissions.PATHWAY_CREATE)\
                and (perm is not Permissions.PATHWAY_UPDATE)\
                and (perm is not Permissions.PATHWAY_DELETE):
            await RolePermission.create(
                role_id=doctor_role.id,
                permission=perm,
            )
        else:
            await RolePermission.create(
                role_id=admin_role.id,
                permission=perm
            )
    return {
        "doctor": doctor_role,
        "admin": admin_role
    }


async def insert_demo_data():
    roles = await create_roles()

    general_milestone_types: Dict[str, MilestoneType] = {
        "referral_letter": await MilestoneType.create(
            name="Referral letter",
            ref_name="Referral letter (record artifact)",
            is_checkbox_hidden=True
        ),
        "chest_xray": await MilestoneType.create(
            name="Chest X-ray",
            ref_name="Plain chest X-ray (procedure)",
            is_test_request=True
        ),
        "ct_chest": await MilestoneType.create(
            name="CT chest",
            ref_name="Computed tomography of chest (procedure)",
            is_test_request=True
        )
    }

    lung_cancer_milestone_types: List[MilestoneType] = [
        await MilestoneType.create(
            name="Pathology",
            ref_name="Pathology report (record artifact)",
            is_checkbox_hidden=True
        ),
        await MilestoneType.create(
            name="Prehab referral",
            ref_name="Prehabilitation (regime/therapy)"
        ),
        await MilestoneType.create(
            name="Dietician referral",
            ref_name="Patient referral to dietitian (procedure)"
        ),
        await MilestoneType.create(
            name="Smoking cessation referral",
            ref_name="Referral to smoking cessation service (procedure)"
        ),
        await MilestoneType.create(
            name="Refer to surgeons",
            ref_name="ref Surgeons",
            is_discharge=True
        ),
        await MilestoneType.create(
            name="Refer to oncology",
            ref_name="ref Oncology",
            is_discharge=True
        ),
        await MilestoneType.create(
            name="Refer to palliation",
            ref_name="ref Palliation",
            is_discharge=True
        ),
        await MilestoneType.create(
            name="Discharge",
            ref_name="ref Discharge",
            is_discharge=True
        ),
        await MilestoneType.create(
            name="Add to MDT",
            ref_name="Assessment by multidisciplinary team (procedure)"
        ),
        await MilestoneType.create(
            name="Book clinic appointment",
            ref_name="Appointment (record artifact)"
        ),
        await MilestoneType.create(
            name="PET-CT",
            ref_name="Positron emission tomography with computed tomography (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="CT head - contrast",
            ref_name="Computed tomography of head with contrast (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="MRI head",
            ref_name="Magnetic resonance imaging of head (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="Lung function tests",
            ref_name="Measurement of respiratory function (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="ECHO",
            ref_name="Echocardiography (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="CT guided biopsy thorax",
            ref_name="Biopsy of thorax using computed tomography guidance (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="EBUS",
            ref_name="Transbronchial needle aspiration using endobronchial ultrasonography guidance (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="ECG",
            ref_name="Electrocardiogram analysis (qualifier value)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="Thoracoscopy",
            ref_name="Thoracoscopy (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="Bronchoscopy",
            ref_name="Bronchoscopy (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="Pleural tap",
            ref_name="Thoracentesis (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="CPET",
            ref_name="Cardiopulmonary exercise test (procedure)",
            is_test_request=True
        ),
        await MilestoneType.create(
            name="Bloods",
            ref_name="Blood test (procedure)",
            is_test_request=True
        ),
    ]

    for pathwayIndex in range(1, NUMBER_OF_PATHWAYS+1):
        pathways: List[Pathway] = [
            await Pathway.create(
                name=f"Lung cancer demo {pathwayIndex}-1"
            ),
            await Pathway.create(
                name=f"Lung cancer demo {pathwayIndex}-2"
            )
        ]

        for key in general_milestone_types:
            await PathwayMilestoneType.create(
                pathway_id=pathways[0].id,
                milestone_type_id=general_milestone_types[key].id
            )
            await PathwayMilestoneType.create(
                pathway_id=pathways[1].id,
                milestone_type_id=general_milestone_types[key].id
            )

        for mT in lung_cancer_milestone_types:
            await PathwayMilestoneType.create(
                pathway_id=pathways[0].id,
                milestone_type_id=mT.id
            )
            await PathwayMilestoneType.create(
                pathway_id=pathways[1].id,
                milestone_type_id=mT.id
            )

        for userIndex in range(1, NUMBER_OF_USERS_PER_PATHWAY+1):
            unencoded_password = f"22password{pathwayIndex}"
            sd_password = hashpw(
                unencoded_password.encode('utf-8'),
                gensalt()
            ).decode('utf-8')
            username = f"demo-{pathwayIndex}-{userIndex}"

            sd_user: User = await User.create(
                username=username,
                password=sd_password,
                email=f"{username}@sd-test.testdomain",
                first_name="Demo",
                last_name=f"User {pathwayIndex} {userIndex}",
                department="Demo user",
            )

            await UserRole.create(
                user_id=sd_user.id,
                role_id=roles['doctor'].id
            )
            if userIndex % 2 == 0:
                await UserRole.create(
                    user_id=sd_user.id,
                    role_id=roles['admin'].id
                )
            
            await UserPathway.create(
                user_id=sd_user.id,
                pathway_id=pathways[0].id
            )
            await UserPathway.create(
                user_id=sd_user.id,
                pathway_id=pathways[1].id
            )

            print(f"Creating user (username: {sd_user.username}; password {unencoded_password}")

        for i in range(1, NUMBER_OF_PATIENTS_PER_PATHWAY+1):

            for pathway in pathways:
                hospital_number_prefix = "fMRN"
                hospital_number = f"{pathway.id}{i}"
                while len(hospital_number) != 6:
                    hospital_number = str(randint(1, 9)) + hospital_number
                hospital_number = hospital_number_prefix + hospital_number

                national_number_prefix = "fNHS"
                national_number = f"{pathway.id}{i}"
                while len(national_number) != 9:
                    national_number = str(randint(1, 9)) + national_number
                national_number = national_number_prefix + national_number

                date_of_birth = date(
                    randint(1950, 1975),
                    randint(1, 12),
                    randint(1, 27)
                )

                sd_patient: Patient = await Patient.create(
                    hospital_number=hospital_number,
                    national_number=national_number
                )

                if isinstance(sd_patient, DataCreatorInputErrors):
                    raise Exception(sd_patient.errorList)

                await PseudoTrustAdapter().create_patient(
                    patient=Patient_IE(
                        first_name=faker.first_name(),
                        last_name=faker.last_name(),
                        hospital_number=hospital_number,
                        national_number=national_number,
                        date_of_birth=date_of_birth,
                        communication_method="LETTER"
                    ),
                    auth_token=SESSION_COOKIE
                )

                sd_onpathway: OnPathway = await OnPathway.create(
                    patient_id=sd_patient.id,
                    pathway_id=pathway.id,
                )

                tie_testresult_ref: TestResult_IE = await PseudoTrustAdapter().create_test_result_immediately(
                    testResult=TestResultRequestImmediately_IE(
                        type_id=general_milestone_types["referral_letter"].id,
                        current_state=MilestoneState.COMPLETED,
                        hospital_number=hospital_number,
                        pathway_name=pathway.name
                    ),
                    auth_token=SESSION_COOKIE
                )

                sd_milestone_ref: Milestone = await Milestone.create(
                    on_pathway_id=sd_onpathway.id,
                    test_result_reference_id=str(tie_testresult_ref.id),
                    current_state=MilestoneState.COMPLETED,
                    milestone_type_id=general_milestone_types["referral_letter"].id,
                )

                tie_testresult_cxr: TestResult_IE = await PseudoTrustAdapter().create_test_result_immediately(
                    testResult=TestResultRequestImmediately_IE(
                        type_id=general_milestone_types["chest_xray"].id,
                        current_state=MilestoneState.COMPLETED,
                        hospital_number=hospital_number,
                        pathway_name=pathway.name
                    ),
                    auth_token=SESSION_COOKIE
                )
                sd_milestone_cxr: Milestone = await Milestone.create(
                    on_pathway_id=sd_onpathway.id,
                    test_result_reference_id=str(tie_testresult_cxr.id),
                    current_state=MilestoneState.COMPLETED,
                    milestone_type_id=general_milestone_types["chest_xray"].id,
                )

                tie_testresult_ctx: TestResult_IE = await PseudoTrustAdapter().create_test_result_immediately(
                    testResult=TestResultRequestImmediately_IE(
                        type_id=general_milestone_types["ct_chest"].id,
                        current_state=MilestoneState.COMPLETED,
                        hospital_number=hospital_number,
                        pathway_name=pathway.name
                    ),
                    auth_token=SESSION_COOKIE
                )
                sd_milestone_ctx: Milestone = await Milestone.create(
                    on_pathway_id=sd_onpathway.id,
                    test_result_reference_id=str(tie_testresult_ctx.id),
                    current_state=MilestoneState.COMPLETED,
                    milestone_type_id=general_milestone_types["ct_chest"].id,
                )


loop = asyncio.get_event_loop()
engine = loop.run_until_complete(db.set_bind(DATABASE_URL))
loop.run_until_complete(check_connection())
loop.run_until_complete(clear_existing_data())
loop.run_until_complete(asyncio.sleep(2))
loop.run_until_complete(insert_demo_data())