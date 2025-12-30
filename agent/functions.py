import os
import json
import datetime
import boto3
from livekit import api
from livekit.agents import function_tool, RunContext, get_job_context
import logging
import random

logger = logging.getLogger(__name__)


SUMMARY_FILE_PATH = "call_summaries.log"   # all summaries stored here

doctor_file_path = os.path.join(os.path.dirname(__file__), "doctors.json")



def generate_id() -> int:
    """Generate a unique positive random ID."""
    return random.randint(100000, 999999)  # 6-digit ID


def write_session_summary(summary_text: str) -> None:
    """
    Appends a structured summary of the call to a single log file.
    Each entry includes:
        - Timestamp
        - Call ID
        - Summary text
    """

    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        call_id = generate_id()

        entry = (
            "\n" +
            "============================================================\n"
            f"CALL SUMMARY — {timestamp}\n"
            f"CALL ID: {call_id}\n"
            "------------------------------------------------------------\n"
            f"{summary_text}\n"
            "============================================================\n"
        )

        # Append to the file (creates the file if it doesn't exist)
        with open(SUMMARY_FILE_PATH, "a", encoding="utf-8") as file:
            file.write(entry)

    except Exception as e:
        print(f"[ERROR] Failed to write call summary: {e}")


# --------------------------
# AWS S3 CONFIGURATION
# --------------------------
# AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
# AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY,
#     region_name=AWS_REGION,
# )

# --------------------------
# FUNCTIONS
# --------------------------

@function_tool()
async def transfer_to_human(ctx: RunContext) -> str:
    """
    Transfers the active SIP participant in the current room
    to a human phone number using LiveKit SIP transfer API.
    """

    # 1. Retrieve the RTC Job Context (required for room access)
    job_ctx = get_job_context()
    if job_ctx is None:
        logger.error("Job context not found")
        return "error"

    # Number or SIP URI to transfer the call to
    transfer_to = "tel:+919515449838"

    # 2. Find the SIP participant in this room
    sip_participant = None
    for participant in job_ctx.room.remote_participants.values():
        if participant.identity.startswith("sip:"):
            sip_participant = participant
            break

    try: 

        if sip_participant is None:
            return "Could not transfer the call..."
        else: 
            await job_ctx.api.sip.transfer_sip_participant(
                api.TransferSIPParticipantRequest(
                    room_name=job_ctx.room.name,
                    participant_identity=sip_participant,
                    transfer_to=transfer_to,
                    play_dialtone=True,
                )
            )
            return "Connecting you to a human agent..."
    except Exception as e:
        logger.error(f"Failed to transfer call: {e}", exc_info=True)
        return "error"


    # if sip_participant is None:
    #     logger.error("No SIP participant found in the room")
    #     return "error"
    # participant_identity = None
    # for p in job_ctx.room.remote_participants.values():
    #     participant_identity = p.identity
    #     print("SIP participant:", p.identity)
    #     break

    # if not participant_identity:
    #     logger.error("No participant identity found in ctx.state['sip_identity']")
    #     return "error"

    # logger.info(
    #     f"Transferring participant {participant_identity} "
    #     f"to {transfer_to}"
    # )

    # # 3. Execute LiveKit SIP Transfer
    # try:
    #     await job_ctx.api.sip.create_sip_outbound_trunk(
    #         api.CreateSIPOutboundTrunkRequest(
    #             room_name=job_ctx.room.name,
    #             participant_identity="agent",  # any identity you want to assign
    #             from_="+14155550000",          # your SIP trunk caller ID
    #             to="tel:+919515449838"         # target phone number
    #         )
    #     )


    #     # logger.info(f"SIP dial result: {result}")
    #     return "Connecting you to a human agent..."
    #     # await job_ctx.api.sip.transfer_sip_participant(
    #     #     api.TransferSIPParticipantRequest(
    #     #         room_name=job_ctx.room.name,
    #     #         participant_identity=participant_identity,
    #     #         transfer_to=transfer_to,
    #     #         play_dialtone=True,
    #     #     )
    #     # )
    #     # return "transferred"

    # except Exception as e:
    #     logger.error(f"Failed to transfer call: {e}", exc_info=True)
    #     return "error"


@function_tool()
async def end_call(ctx: RunContext) -> str:
    """
    Ends the current LiveKit room call.
    This is used when the user is not interested, wants to stop,
    or all questions are answered.
    """

    # 1. Get RTC Job Context
    job_ctx = get_job_context()
    if job_ctx is None:
        logger.error("Failed to get job context")
        return "error"

    room_name = job_ctx.room.name
    logger.info(f"Ending call for room {room_name}")

    # 2. Attempt to delete room → this ends the call
    try:
        await job_ctx.api.room.delete_room(
            api.DeleteRoomRequest(
                room=job_ctx.room.name,
            )
        )

        logger.info(f"Successfully ended call for room {room_name}")
        return "ended"

    except Exception as e:
        logger.error(f"Failed to end call: {e}", exc_info=True)
        return "error"


@function_tool()
async def save_appointment(
    customer_name: str,
    age: str,
    phone: str,
    address: str,
    symptoms: str,
    doctor_name: str,
    time_slot: str
) -> str:
    """
    Save appointment, update doctor availability,
    and return booking_id. If error → return -1.
    """
    try:
        timestamp = datetime.datetime.now().isoformat()
        booking_id = generate_id()

        # ---------------------------
        # 1. Save appointment details
        # ---------------------------
        data = {
            "booking_id": booking_id,
            "customer_name": customer_name,
            "age": age,
            "phone": phone,
            "address": address,
            "symptoms": symptoms,
            "doctor_name": doctor_name,
            "time_slot": time_slot,
            "saved_at": timestamp
        }

        with open("appointments.jsonl", "a") as f:
            f.write(json.dumps(data) + "\n")

        # ---------------------------
        # 2. Remove booked time slot
        # ---------------------------
        try:
            slot_date, slot_time = time_slot.split(" | ")
        except ValueError:
            # Slot format wrong → Return ID anyway but warn in logs
            return str(booking_id)

        with open(doctor_file_path, "r") as f:
            doctors_data = json.load(f)

        for specialist, doctors in doctors_data.items():
            for doctor in doctors:
                if doctor["doctor_name"] == doctor_name:

                    if slot_date in doctor["available_slots"]:
                        if slot_time in doctor["available_slots"][slot_date]:
                            doctor["available_slots"][slot_date].remove(slot_time)

                            if len(doctor["available_slots"][slot_date]) == 0:
                                del doctor["available_slots"][slot_date]

                    break

        with open(doctor_file_path, "w") as f:
            json.dump(doctors_data, f, indent=4)

        return str(booking_id)

    except Exception as e:
        print(f"[ERROR] Failed to save appointment: {e}")
        return "-1"


@function_tool()
async def save_medicine_refill_order(
    customer_name: str,
    age: str,
    address: str,
    medicine_name: str,
    quantity: str,
    usage_duration: str,
    consulted_doctor: str,
    instructions: str
) -> str:
    """
    Save prescription order with unique refill_id.
    Return refill_id if success, else -1.
    """
    try:
        timestamp = datetime.datetime.now().isoformat()
        refill_id = generate_id()

        data = {
            "refill_id": refill_id,
            "customer_name": customer_name,
            "age": age,
            "address": address,
            "medicine_name": medicine_name,
            "quantity": quantity,
            "usage_duration": usage_duration,
            "consulted_doctor": consulted_doctor,
            "instructions": instructions,
            "saved_at": timestamp
        }

        with open("prescriptions.jsonl", "a") as f:
            f.write(json.dumps(data) + "\n")

        return str(refill_id)

    except Exception as e:
        print(f"[ERROR] Failed to save refill order: {e}")
        return "-1"

@function_tool()
async def get_doctors_list(specialist: str) -> str:
    """
    Returns list of doctors and their available time slots
    from the doctors.json file for the specified specialist.
    """

    # -------- Load doctor data from JSON file --------
    # doctor_file_path = doctor_file_path

    if not os.path.exists(doctor_file_path):
        return json.dumps({
            "error": "doctors.json file not found in project directory."
        })

    try:
        with open(doctor_file_path, "r") as f:
            doctors_db = json.load(f)
    except Exception as e:
        return json.dumps({
            "error": f"Failed to read doctors.json: {str(e)}"
        })

    # Convert specialist input into key format
    specialist_key = specialist.lower().replace(" ", "_")

    if specialist_key not in doctors_db:
        return json.dumps({
            "error": f"No doctors found for specialization '{specialist}'."
        })

    # -------- Return filtered doctor list --------
    return json.dumps({
        "specialization": specialist,
        "doctors": doctors_db[specialist_key]
    })



# @function_tool()
# async def save_audio_recording(recording_url: str) -> str:
#     """
#     Save audio recording to S3 from a recording URL.
#     """
#     import requests

#     try:
#         audio_data = requests.get(recording_url).content
#         file_key = f"recordings/{datetime.datetime.now().timestamp()}.wav"

#         s3_client.put_object(
#             Bucket=AWS_BUCKET_NAME,
#             Key=file_key,
#             Body=audio_data,
#             ContentType="audio/wav"
#         )

#         return f"Recording saved to S3 as {file_key}"

#     except Exception as e:
#         return f"Failed to save recording: {str(e)}"
