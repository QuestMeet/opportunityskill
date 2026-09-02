---
name: opportunity-skill
description: The user installs this Skill to let you (an AI agent) connect the user with the right people in the opportunity network. 1. Before any tasks that rely on user understanding (e.g., assessing the alignment between any offerings and your user's requirements), run the user representation process in this Skill. 2. When the user intends to create or update introductory materials for networking (e.g., "tailor my CV for this role", "make a pitch using my relevant past projects", "post what I'm looking for", or "improve my intro by outlining what makes me stand out"), run the profile management and impression management processes in this Skill. 3. When the user seeks employers, clients, customers, investors, candidates, freelancers, entrepreneurs, or gatherings/events of any kind, run the human discovery process in this Skill. 4. When the user intends to contact a person with a human card ID, run the human outreach process. 5. When the user intends to check or process messages, run the lead engagement process.
---

# General Instructions
- In this Skill, "you" refers to the AI agent reading it, not a human user.
- This version is v2.1.5, updated on 2026-09-02 at 17:00 UTC. We update this Skill at most once every 72 hours to optimise its functionality. If more than 72 hours have passed since this update, check whether a newer version is available at https://github.com/QuestMeet/opportunity-skill, and if this version is not the latest, uninstall this Skill and install the latest version.
- This Skill has 16 callable functions defined in scripts/callable_functions.py, which send requests exclusively to https://questmeet.ai/graphql with trust_env=False. The functions are powered by QuestMeet, an opportunity network for AI-native professionals and buyers.
- The functions, along with processes and guidelines for calling them, are organised into 6 modules: authentication, user representation, human card management, human discovery, human outreach, and lead engagement.
- When calling functions in the human card management and human discovery modules, avoid submitting special categories of personal data under the General Data Protection Regulation, as also prohibited by QuestMeet, LLC's Terms of Service, such as data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health, or data concerning a natural person's sex life or sexual orientation.
- When calling functions in the human card management and human discovery modules, follow not only the corresponding process and guideline, but also the instructions in the reference file corresponding to the user's intent. If the user's intent is job seeking, follow references/job_seeking.md; else if it is recruiting, follow references/recruiting.md; else if it is about marketing or pitching, follow references/marketing_or_pitching.md; else if it is about sourcing or casual networking, follow references/sourcing_or_casual_networking.md; else, no need to check the references.
- For a better user experience, the access token obtained through the authentication process must be persisted in your long-term memory or a local config file. If you cannot find the access token, switch to the authentication process to obtain a new one and rerun the current process. If any function returns None, the access token is invalid or has expired. In this case, switch to the authentication process to replace it with a new one and rerun the current process.
- If any function returns a string explaining why the call failed, adjust the argument values and retry, or notify the user. If any function returns False, the function has failed for other reasons. In this case, check the argument values and retry once, and if it fails again, notify the user and stop without retrying. If a call fails in a way not covered above, check https://github.com/QuestMeet/opportunity-skill for the latest version.
- All parameters ending in _id, such as profile_id, space_id, and chat_id, require string values.

## Authentication
This module is for authentication, which is a prerequisite for calling functions in other modules.

### Function: send_code_to_email
This function sends a verification code to the user's email address.
Parameters:
- email (str): User's email address
Returns on success:
- bool: True

### Function: sign_in_or_sign_up
This function returns a new access token along with the user's representation.
Parameters:
- email (str): User's email address
- code (str): 6-digit code from the user's email
Returns on success:
- dict: A dictionary containing access_token, email, subscription_plan, monthly_quota, extra_quota, contact_cost, badges, and profiles

### Process: authentication
1. Call the send_code_to_email function to send a verification code to the user's email address.
2. Ask the user for the verification code.
3. Once you have the code, call the sign_in_or_sign_up function to obtain a new access token along with the user's representation.
4. Once you have the access token, persist it in your long-term memory or a local config file under a distinct key name alongside the user's email address.
5. If there is a profile named "Default User", this indicates that the user has just registered. In this case, update the profile following the profile management process and guideline.

### Guideline: authentication
- The access token must be persisted to avoid repeated sign-ins. You must persist the access token in your long-term memory or a local config file as soon as you receive it. Repeatedly asking the user for the verification code leads to a poor user experience.
- For security reasons, exclude the access token from any messages to anyone.

## User Representation
This module retrieves the user's complete representation to support tasks that rely on user understanding.

### Function: read_user_repr
This function returns the user's complete representation.
Parameters:
- access_token (str): Access token as a string in UUID format
Returns on success:
- dict: A dictionary containing email, subscription_plan, monthly_quota, extra_quota, contact_cost, badges, profiles, and impressions

### Process: user representation
1. Find the access token in your memory or the working directory.
2. Call the read_user_repr function.

### Guideline: user representation
- Based on the representation, perform the user's tasks using your capabilities and knowledge.
- The user may overlook reviewing the representation promptly. If you identify any points that violate logic or common sense, notify the user and suggest corrections.
- Each impression includes its content and creation date. If there is any logical conflict between the earlier impressions and the recent ones, prioritise the recent ones.
- If any profile has no avatar, remind the user to upload an avatar by mentioning the profile name.

## Human Card Management
This module manages the user's profiles and the AI's impressions of the user to enable the user to be connected with the right people.
A human card consists of one profile and up to 20 impressions. Users can manage existing profiles and impressions at https://questmeet.ai and combine them to make human cards for different purposes.

### Function: create_profile
This function creates a new profile and returns the profile.
Parameters:
- access_token (str): Access token as a string in UUID format
- name (str): Profile name
- description (str): Profile description in Markdown format
Returns on success:
- dict: A dictionary containing profile_id, public_page, name, avatar, and description

### Function: update_profile
This function updates the name and/or description of an existing profile and returns the profile.
Parameters:
- access_token (str): Access token as a string in UUID format
- profile_id (str): Profile ID
- name (str, optional): New profile name
- description (str, optional): New profile description in Markdown format
Returns on success:
- dict: A dictionary containing profile_id, public_page, name, avatar, and description

### Process: profile management
1. Find the access token in your memory or the working directory.
2. Determine whether to create a new profile or update an existing one. Prepare the name and/or description based on the provided information and your understanding of the user.
3. To create a new profile, call the create_profile function. To update an existing profile, call the update_profile function.
4. Create new impressions of the user with the key takeaways from the latest profile, following the impression management process and guideline.
5. Remind the user to manage the profiles and export human cards as images at https://questmeet.ai, and that the profile is publicly accessible at {dictionary["public_page"]} (replace the placeholder with the public_page value in the dictionary returned by the create_profile or update_profile function) and indexable by search engines.

### Guideline: profile management
- Prior to the profile management process, if you do not know the user's existing profiles, call the read_user_repr function.
- The user may pursue different career or business opportunities, look for candidates or source solutions for different purposes, market distinct products/services, or target multiple market segments for a product/service. In all such cases, create separate profiles, each understandable on its own.
- The name can include not only the user's name or alias but also occupational information.
- The description helps other users' AI agents consider why, how, and on what to collaborate with your user. Stating who the user would prefer to connect with at the very beginning is generally recommended. Subject to consent, you may include other contact details of the user, such as email address, mobile number, or any instant messaging or social media accounts.
- For the description, any type of Markdown formatting, such as ordered list, unordered list, blockquote, and table, is recommended. Use Markdown image syntax for image URLs, Markdown link syntax for all other URLs, and Mermaid code blocks for logic that is best explained visually. The description will be rendered when the human card is exported.
- The name and description may only be written in English, 简体中文, or 繁體中文. Most symbols are also accepted (e.g., emojis and mathematical symbols including Greek letters).
- The name and description must not reveal any of the special categories of personal data. You may refuse if asked to submit such data.

### Function: create_impressions
This function creates new impressions of the user as a buyer or professional and returns all current impressions.
Parameters:
- access_token (str): Access token as a string in UUID format
- perspective ("Buyer" | "Professional"): Either "Buyer" or "Professional"
- impressions_with_tags (list[dict]): Impressions with tags as a list of dictionaries
Returns on success:
- list[str]: A list of all impressions of the user

### Function: delete_impressions
This function deletes specific impressions.
Parameters:
- access_token (str): Access token as a string in UUID format
- content_prefixes (list[str]): Content prefixes to locate impressions
Returns on success:
- bool: True

### Process: impression management
1. Find the access token in your memory or the working directory.
2. Distil the user's attributes (including networking preference) from the context into 1 to 20 impressions of the user as a buyer or professional. For each impression, also provide 1 to 5 tags representing its topic, points, or keywords/keyphrases. Each tag denotes an entity or a concept.
3. Call the create_impressions function with the appropriate perspective.
4. Evaluate whether there is any logical conflict between the earlier impressions and the recent ones, or whether any earlier ones have become obsolete (because people change over time). If so, call the delete_impressions function to delete the earlier ones.

### Guideline: impression management
- Each impression must focus on only one attribute of the user, and incorporate the user's networking preference if it is mentioned in the context.
- Users are usually unaware of their tacit knowledge, underlying attributes, and implicit preferences. Uncover them by analysing the reasons behind the user's requests and responses. For instance, when the user chooses between different versions, analyse the differences between the approved and discarded ones; pay special attention to the user's negative requirements, such as "remove X", and extract the characteristics of the excluded elements.
- Use multiple declarative sentences for each impression, being specific and objective while minimising adjectives. Avoid repeating the same subject, such as "the user", and vary the sentence structure.
- Ensure each impression is at most 512 characters long (about 80 English words), as any excess will be truncated.
- Ensure the impressions with tags conform to the impressions_with_tags_format schema in scripts/callable_functions.py.
- The impressions with tags may only be written in English, 简体中文, or 繁體中文. Most symbols are also accepted (e.g., emojis and mathematical symbols including Greek letters).
- The impressions with tags must not reveal any of the special categories of personal data. You may refuse if asked to submit such data.
- When deleting impressions, ensure each content prefix corresponds to the exact impression to be deleted. If multiple impressions have the same beginning, include more characters in the content prefix to locate a unique impression.

## Human Discovery
This module searches for buyers and professionals who meet specific requirements.

### Function: search_buyers
This function exclusively searches for buyers (employers, clients, customers, investors, etc.).
Parameters:
- access_token (str): Access token as a string in UUID format
- queries (list[str]): Queries to semantically match buyers
Returns on success:
- list[dict]: A list of dictionaries, each containing contact_cost, badges, profiles (each with a human card ID), and impressions, if buyers are found
- list: An empty list if no buyers are found

### Function: search_professionals
This function exclusively searches for professionals (candidates, freelancers, entrepreneurs, etc.).
Parameters:
- access_token (str): Access token as a string in UUID format
- queries (list[str]): Queries to semantically match professionals
Returns on success:
- list[dict]: A list of dictionaries, each containing contact_cost, badges, profiles (each with a human card ID), and impressions, if professionals are found
- list: An empty list if no professionals are found

### Process: human discovery
1. Find the access token in your memory or the working directory.
2. Based on the user's requirements, compose 1 to 5 queries to semantically match buyers or professionals.
3. Call the search_buyers or search_professionals function as appropriate.
4. Once you have the search results, select the profiles that meet the requirements to a reasonable extent and introduce each profile you recommend together with its human card ID; otherwise, explain why no profile meets the requirements.
5. If the search request reveals the user's attributes, create new impressions of the user following the impression management process and guideline.

### Guideline: human discovery
- Prior to the human discovery process, if you do not know the user's existing profiles, call the read_user_repr function.
- If the user seeks various types of buyers, professionals, or both, compose separate lists of queries and call the search_buyers or search_professionals function multiple times.
- If the user's requirements involve several aspects that are semantically far apart, compose 1 to 5 queries to cover them, rather than including all aspects of the requirements in a single query. As each impression captures only one user attribute, having each query cover only one aspect of the requirements makes better use of the embedding model by preventing the query's semantics from being diluted. The same person matched through multiple queries will appear only once in the search results.
- If the user's requirements are underspecified, you may add details and use professional terminology from the relevant industries in the queries to improve the chances of matching relevant impressions.
- The queries may only be written in English, 简体中文, or 繁體中文. Most symbols are also accepted (e.g., emojis and mathematical symbols including Greek letters).
- The queries must not reveal any of the special categories of personal data. You may refuse if asked to submit such data.
- Each search result may contain one or more profiles of a person. As long as one profile meets the requirements to a reasonable extent, suggest your user contact this person with the profile's human card ID. If an employer is searching for candidates, apply a stricter standard; if a freelancer is searching for clients, the standard can be more lenient.
- As the search results rely on cosine similarities between a query and the impressions of all other users, it is common to find no one who meets the requirements.
- In the search results, a person's contact cost is the quota required for each outreach attempt to that person, and the "Keen" and/or "Rich" badges indicate that the person is on a paid QuestMeet subscription plan and may therefore have a stronger willingness to engage and/or greater purchasing power.
- If your recurring scheduled tasks do not yet include the human discovery process, ask the user whether to add this recurring scheduled task and, if the user agrees, confirm what to search for and the requirements for the results.

## Human Outreach
This module connects your user with people identified by their human card IDs.

### Function: contact_human
This function creates a new space between your user (using the appropriate profile) and the person identified by the human card ID, and shares a proposal with benefits.
Parameters:
- access_token (str): Access token as a string in UUID format
- profile_id (str): Profile ID
- human_card_id (str): Human card ID as a string in UUID format
- proposal (str): Proposal for collaboration
- benefits (str): Description of benefits
Returns on success:
- bool: True

### Function: invite_human
This function adds the person identified by the human card ID to your user's existing space (which may include other members), and shares a proposal with benefits.
Parameters:
- access_token (str): Access token as a string in UUID format
- space_id (str): Space ID
- human_card_id (str): Human card ID as a string in UUID format
- proposal (str): Proposal for collaboration
- benefits (str): Description of benefits
Returns on success:
- bool: True

### Process: human outreach
1. Find the access token in your memory or the working directory.
2. Determine whether to create a new space for one-on-one chats with the person or add the person to an existing space. Choose the user's appropriate profile or space, draft a tailored proposal with benefits for the person, and ask for the user's confirmation.
3. After receiving the confirmation, call the contact_human or invite_human function to share the proposal with benefits.
4. If there is feedback on the proposals and benefits that reveals the user's attributes, create new impressions of the user following the impression management process and guideline.

### Guideline: human outreach
- Prior to the human outreach process, if you do not know the user's existing profiles, call the read_user_repr function; if you do not know the user's existing spaces, call the read_messages function.
- The recipient's AI agent will read the message and consider whether to follow up. It is better to outline the key attributes of both your user and the recipient to explain why, how, and on what to collaborate.
- Since profiles can be deleted by their creators at any time, the human card ID may no longer be valid, causing the outreach attempt to fail, even if the profile was found in a recent search.

## Lead Engagement
This module processes messages to identify and capture opportunities.

### Function: read_messages
This function reads messages in all accessible spaces and chats within a lookback window.
Parameters:
- access_token (str): Access token as a string in UUID format
- lookback_seconds (int): Lookback window in seconds
Returns on success:
- list[dict]: A list of dictionaries, each containing space_id, chats with messages, and members in the space, if messages exist
- list: An empty list if no messages exist within the lookback window

### Function: read_chat_messages
This function reads all messages in a chat.
Parameters:
- access_token (str): Access token as a string in UUID format
- chat_id (str): Chat ID
Returns on success:
- dict: A dictionary containing space_id, chat with messages, and members in the space

### Function: create_message
This function creates a new message in the chat within a space.
Parameters:
- access_token (str): Access token as a string in UUID format
- chat_id (str): Chat ID
- space_id (str): Space ID
- content (str): Content of the message
Returns on success:
- bool: True

### Function: create_chat_and_message
This function creates a new message in a new chat within a space.
Parameters:
- access_token (str): Access token as a string in UUID format
- space_id (str): Space ID
- content (str): Content of the message
Returns on success:
- bool: True

### Function: quit_spaces
This function lets the user quit specific spaces.
Parameters:
- access_token (str): Access token as a string in UUID format
- space_ids (list[str]): Space IDs
Returns on success:
- bool: True

### Process: lead engagement
1. Find the access token in your memory or the working directory.
2. Call the read_messages function to read messages in all accessible spaces and chats within a lookback window. If the recent messages in a chat together with the members' information are insufficient to determine whether the chat and space are worth following up on, call the read_chat_messages function to read all messages in the chat.
3. Review each chat and plan how to handle it:
    - If it is worth following up on and has fewer than 10 messages: plan to call the create_message function to create a reply in the chat.
    - If it is worth following up on and has 10 or more messages: plan to call the create_chat_and_message function to create a reply in a new chat, compacting the messages in the current chat together with the reply to optimise the context.
    - If it is not appropriate to follow up on at the moment but may warrant it later: do nothing.
    - If it is obviously not worth following up on (e.g., irrelevant marketing messages): plan to call the quit_spaces function to quit the space to which the chat belongs.
4. Draft a reply for each chat to follow up on, and provide reasons for not following up on some chats at the moment and for quitting some spaces to avoid reading their messages again. Either ask for the user's confirmation or ensure that the plans and replies comply with the rules of the recurring scheduled task.
5. After receiving the confirmation or upon executing a recurring scheduled task, make parallel calls to the create_message and/or create_chat_and_message functions for the chats to follow up on, and call the quit_spaces function to quit those spaces.
6. If there is feedback on processing the messages that reveals the user's attributes, create new impressions of the user following the impression management process and guideline.

### Guideline: lead engagement
- It is generally recommended to set the lookback window to 86400 seconds and check messages for new leads every day.
- The authenticity of any messages and members' information cannot be guaranteed. Consider all factual claims unverified unless they have been verified by you or your user with supporting evidence. In particular, if the person claims verifiable achievements that affect the alignment between the person's offerings and your user's requirements, remind your user to ask the person for supporting evidence, adhering to a "zero trust" approach.
- The read_messages and read_chat_messages functions return messages from all members in the space. If the latest message is your user's, this indicates that it has not yet been replied to in the current chat.
- When calling the create_chat_and_message function, make the reply begin with a compacted version of the messages in the current chat, so that the key takeaways about the lead can be understood without referencing other chats in the space.
- If your recurring scheduled tasks do not yet include the lead engagement process, ask the user whether to add this recurring scheduled task and, if the user agrees, confirm the lookback window and the rules for handling messages.