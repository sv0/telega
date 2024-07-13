"""
Utils and helpers for telega web application.

Functions `get_human_readable_user_status` and `get_user_by_phone`
came from https://github.com/bellingcat/telegram-phone-number-checker :
See telegram_phone_number_checker/main.py

Copyright (c) 2021 Stichting Bellingcat

Copyright (c) 2024 Slavik Svyrydiuk
"""
from telethon.sync import TelegramClient, functions
from telethon.tl import types


def get_human_readable_user_status(status: types.TypeUserStatus):
    match status:
        case types.UserStatusOnline():
            return "Currently online"
        case types.UserStatusOffline():
            return status.was_online.strftime("%Y-%m-%d %H:%M:%S %Z")
        case types.UserStatusRecently():
            return "Last seen recently"
        case types.UserStatusLastWeek():
            return "Last seen last week"
        case types.UserStatusLastMonth():
            return "Last seen last month"
        case _:
            return "Unknown"


async def get_user_by_phone(client: TelegramClient, phone_number: str) -> dict:
    """Take in telegram client instance and phone number.
       Returns the associated user information if the user exists.

       It does so by first adding the user's phones to the contact list,
       retrieving the information, and then deleting the user
       from the contact list.
    """
    result = {}
    try:
        # Create a contact
        contact = types.InputPhoneContact(
            client_id=0, phone=phone_number, first_name="", last_name=""
        )
        # Attempt to add the contact from the address book
        contacts = await client(
            functions.contacts.ImportContactsRequest([contact])
        )

        users = contacts.to_dict().get("users", [])

        if not users:
            result.update({
                "error": "No response, the phone number is not on Telegram"
                         " or has blocked contact adding."
            })
        elif len(users) == 1:
            # Attempt to remove the contact from the address book.
            # The response from DeleteContactsRequest contains more information
            # than from ImportContactsRequest
            updates_response: types.Updates = await client(
                functions.contacts.DeleteContactsRequest(id=[users[0].get("id")])  # noqa
            )
            user = updates_response.users[0]
            # getting more information about the user
            result.update(
                {
                    "id": user.id,
                    "username": user.username,
                    "usernames": user.usernames,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "fake": user.fake,
                    "verified": user.verified,
                    "premium": user.premium,
                    "mutual_contact": user.mutual_contact,
                    "bot": user.bot,
                    "bot_chat_history": user.bot_chat_history,
                    "restricted": user.restricted,
                    "restriction_reason": user.restriction_reason,
                    "user_was_online": get_human_readable_user_status(user.status),  # noqa
                    "phone": user.phone or phone_number,
                }
            )
        else:
            result.update({
                "error": "This phone number matched multiple \
                          Telegram accounts, which is unexpected."
                }
            )

    except TypeError as err:
        result.update({
            "error": f"TypeError: {err}. \
                       The error might have occurred due to the inability to \
                       delete the {phone_number=} from the contact list."
        })
    except Exception as err:
        result.update({"error": f"Unexpected error: {err}."})
    return result
