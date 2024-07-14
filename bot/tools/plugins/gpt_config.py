import logging
import os

from dotenv import load_dotenv

load_dotenv(os.path.abspath("config.env"))
gpt_config = {
    'model': os.environ.get("OPENAI_MODEL"),
    'api_key': os.environ.get('OPENAI_API_KEY'),
    'max_tokens': int(os.environ.get("MAX_TOKENS")),
    'max_history_size': int(os.environ.get("MAX_HISTORY_SIZE")),
    'temperature': float(os.environ.get("TEMPERATURE")),
    'assistant_prompt': os.environ.get('ASSISTANT_PROMPT'),
    'token': os.environ.get('TELEGRAM_BOT_TOKEN'),
    'admin_user_ids': os.environ.get('ADMIN_USER_IDS', 'ADMIN_1_USER_ID,ADMIN_2_USER_ID').split(','),
    'allowed_user_ids': os.environ.get('ALLOWED_TELEGRAM_USER_IDS', 'USER_ID_1,USER_ID_2').split(','),
    'enable_functions': os.environ.get("ENABLE_FUNCTIONS"),
    'enable_quoting': os.environ.get('ENABLE_QUOTING').lower() == 'true',
    'enable_image_generation': os.environ.get('ENABLE_IMAGE_GENERATION').lower() == 'true',
    'enable_transcription': os.environ.get('ENABLE_TRANSCRIPTION').lower() == 'true',
    'enable_vision': os.environ.get('ENABLE_VISION').lower() == 'true',
    'enable_tts_generation': os.environ.get('ENABLE_TTS_GENERATION').lower() == 'true',
    'budget_period': os.environ.get('BUDGET_PERIOD').lower(),
    'user_budgets': os.environ.get('USER_BUDGETS'),
    'guest_budget': float(os.environ.get('GUEST_BUDGET')),
    'stream': os.environ.get('STREAM').lower() == 'true',
    'proxy': os.environ.get('PROXY') or os.environ.get('TELEGRAM_PROXY'),
    'voice_reply_transcript': os.environ.get('VOICE_REPLY_WITH_TRANSCRIPT_ONLY').lower() == 'true',
    'voice_reply_prompts': os.environ.get('VOICE_REPLY_PROMPTS').split(';'),
    'ignore_group_transcriptions': os.environ.get('IGNORE_GROUP_TRANSCRIPTIONS').lower() == 'true',
    'ignore_group_vision': os.environ.get('IGNORE_GROUP_VISION').lower() == 'true',
    'group_trigger_keyword': os.environ.get('GROUP_TRIGGER_KEYWORD'),
    'token_price': float(os.environ.get('TOKEN_PRICE')),
    'image_prices': [float(i) for i in os.environ.get('IMAGE_PRICES').split(",")],
    'vision_token_price': float(os.environ.get('VISION_TOKEN_PRICE')),
    'image_receive_mode': os.environ.get('IMA   GE_FORMAT'),
    'tts_model': os.environ.get('TTS_MODEL'),
    'tts_prices': [float(i) for i in os.environ.get('TTS_PRICES').split(",")],
    'transcription_price': float(os.environ.get('TRANSCRIPTION_PRICE')),
    'bot_language': os.environ.get('BOT_LANGUAGE'),
    'n_choices': int(os.environ.get('N_CHOICES')),
    'openai_base_url': os.environ.get('OPENAI_BASE_URL'),
    'show_usage': os.environ.get('SHOW_USAGE').lower() == 'false',
    'max_conversation_age_minutes': int(os.environ.get('MAX_CONVERSATION_AGE_MINUTES')),
    'vision_prompt': os.environ.get('VISION_PROMPT'),
    'vision_max_tokens': int(os.environ.get('VISION_MAX_TOKENS')),
    'presence_penalty': float(os.environ.get('PRESENCE_PENALTY')),
    'frequency_penalty': float(os.environ.get('FREQUENCY_PENALTY')),
    'image_model': os.environ.get('IMAGE_MODEL'),
    'image_quality': os.environ.get('IMAGE_QUALITY'),
    'image_style': os.environ.get('IMAGE_STYLE'),
    'image_size': os.environ.get('IMAGE_SIZE'),
    'vision_detail': os.environ.get('VISION_DETAIL'),
    'enable_vision_follow_up_questions': os.environ.get('ENABLE_VISION_FOLLOW_UP_QUESTIONS').lower() == 'true',
    'vision_model': os.environ.get('VISION_MODEL'),
    'db_connection_url': os.environ.get('DB_CONNECTION_URL')
}

plugin_config = {
        'plugins': os.environ.get('plugins', '').split(',')
    }
