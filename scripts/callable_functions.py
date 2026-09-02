import httpx
import jsonschema
from typing import Union

BASE_URL = "https://questmeet.ai/graphql"

def send_code_to_email(email: str) -> bool:
    response = httpx.post(BASE_URL, json={"query": "mutation SendCodeToEmail($email: String!) { sendCodeToEmail(email: $email) }", "variables": {"email": email}}, trust_env=False, timeout=20)
    return response.json()["data"]["sendCodeToEmail"]

def sign_in_or_sign_up(email: str, code: str) -> Union[dict, str, bool]:
    response = httpx.post(BASE_URL, json={"query": "mutation SignInOrSignUp($email: String!, $code: String!) { signInOrSignUp(email: $email, code: $code) }", "variables": {"email": email, "code": code}}, trust_env=False, timeout=20)
    return response.json()["data"]["signInOrSignUp"]

def read_user_repr(access_token: str) -> Union[dict, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "query ReadUserRepr { readUserRepr }"}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["readUserRepr"]

impressions_with_tags_format = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "impression": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 5}
        },
        "required": ["impression", "tags"],
        "additionalProperties": False
    }
}

def create_impressions(access_token: str, perspective: str, impressions_with_tags: list) -> Union[list, str, bool, None]:
    jsonschema.validate(instance=impressions_with_tags, schema=impressions_with_tags_format)
    response = httpx.post(BASE_URL, json={"query": "mutation CreateImpressions($perspective: String!, $impressionsWithTags: JSON!) { createImpressions(perspective: $perspective, impressionsWithTags: $impressionsWithTags) }", "variables": {"perspective": perspective, "impressionsWithTags": impressions_with_tags}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=60)
    return response.json()["data"]["createImpressions"]

def delete_impressions(access_token: str, content_prefixes: list[str]) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation DeleteImpressions($contentPrefixes: [String!]!) { deleteImpressions(contentPrefixes: $contentPrefixes) }", "variables": {"contentPrefixes": content_prefixes}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["deleteImpressions"]

def create_profile(access_token: str, name: str, description: str) -> Union[dict, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation CreateProfile($name: String!, $description: String!) { createProfile(name: $name, description: $description) }", "variables": {"name": name, "description": description}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["createProfile"]

def update_profile(access_token: str, profile_id: str, name: str = None, description: str = None) -> Union[dict, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation UpdateProfile($profileId: BigInt!, $name: String, $description: String) { updateProfile(profileId: $profileId, name: $name, description: $description) }", "variables": {"profileId": profile_id, "name": name, "description": description}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["updateProfile"]

def search_buyers(access_token: str, queries: list[str]) -> Union[list, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "query SearchBuyers($queries: [String!]!) { searchBuyers(queries: $queries) }", "variables": {"queries": queries}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=60)
    return response.json()["data"]["searchBuyers"]

def search_professionals(access_token: str, queries: list[str]) -> Union[list, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "query SearchProfessionals($queries: [String!]!) { searchProfessionals(queries: $queries) }", "variables": {"queries": queries}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=60)
    return response.json()["data"]["searchProfessionals"]

def contact_human(access_token: str, profile_id: str, human_card_id: str, proposal: str, benefits: str) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation ContactHuman($profileId: BigInt!, $humanCardId: String!, $proposal: String!, $benefits: String!) { contactHuman(profileId: $profileId, humanCardId: $humanCardId, proposal: $proposal, benefits: $benefits) }", "variables": {"profileId": profile_id, "humanCardId": human_card_id, "proposal": proposal, "benefits": benefits}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["contactHuman"]

def invite_human(access_token: str, space_id: str, human_card_id: str, proposal: str, benefits: str) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation InviteHuman($spaceId: BigInt!, $humanCardId: String!, $proposal: String!, $benefits: String!) { inviteHuman(spaceId: $spaceId, humanCardId: $humanCardId, proposal: $proposal, benefits: $benefits) }", "variables": {"spaceId": space_id, "humanCardId": human_card_id, "proposal": proposal, "benefits": benefits}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["inviteHuman"]

def read_messages(access_token: str, lookback_seconds: int) -> Union[list, str, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "query ReadMessages($lookbackSeconds: Int!) { readMessages(lookbackSeconds: $lookbackSeconds) }", "variables": {"lookbackSeconds": lookback_seconds}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["readMessages"]

def read_chat_messages(access_token: str, chat_id: str) -> Union[dict, bool, None]:
    response = httpx.post(BASE_URL, json={"query": "query ReadChatMessages($chatId: BigInt!) { readChatMessages(chatId: $chatId) }", "variables": {"chatId": chat_id}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["readChatMessages"]

def create_message(access_token: str, chat_id: str, space_id: str, content: str) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation CreateMessage($chatId: BigInt!, $spaceId: BigInt!, $content: String!) { createMessage(chatId: $chatId, spaceId: $spaceId, content: $content) }", "variables": {"chatId": chat_id, "spaceId": space_id, "content": content}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["createMessage"]

def create_chat_and_message(access_token: str, space_id: str, content: str) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation CreateChatAndMessage($spaceId: BigInt!, $content: String!) { createChatAndMessage(spaceId: $spaceId, content: $content) }", "variables": {"spaceId": space_id, "content": content}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["createChatAndMessage"]

def quit_spaces(access_token: str, space_ids: list[str]) -> Union[bool, None]:
    response = httpx.post(BASE_URL, json={"query": "mutation QuitSpaces($spaceIds: [BigInt!]!) { quitSpaces(spaceIds: $spaceIds) }", "variables": {"spaceIds": space_ids}}, headers={"Authorization": f"Bearer {access_token}"}, trust_env=False, timeout=20)
    return response.json()["data"]["quitSpaces"]