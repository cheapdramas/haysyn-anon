from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import File, Message, FSInputFile
from pydub import AudioSegment
from core.config import VOICE_MESSAGES_PATH
from core.messages import SENT_SUCCESS, SENT_FAILURE, message_anon 
from keyboards.reply import keyboard_reply_menu
from keyboards.inline import keyboard_anon_message
import os

filters = []

def apply_voice_filter(input_path: str, output_path: str):
    """applies filter on voice message, and saves it as <output_path>"""
    audio = AudioSegment.from_file(input_path)
    
    # apply a downgrade pitch filter
    audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 0.6)})
    audio = audio.set_frame_rate(48000)

    audio.export(output_path, format="ogg", codec="libopus", parameters=["-application", "voip"])


async def handle_voice_message(message: Message, bot: Bot, state: FSMContext):
    input_path = None
    output_path = None
    try:
        voice = message.voice
        file: File = await bot.get_file(voice.file_id)
        file_path = file.file_path

        # Get voice file bytes
        downloaded = await bot.download_file(file_path)
        # Path for original voice message 
        input_path = VOICE_MESSAGES_PATH / f"{voice.file_id}.ogg"
        # Write original voice message into input_path
        with open(input_path, "wb") as f:
            f.write(downloaded.read())

        await message.answer("<i>Обробляю голосове...</i>",parse_mode="HTML")
       
        # Path for filtered message
        output_path = VOICE_MESSAGES_PATH / f"{voice.file_id}filtered.ogg"
        
        apply_voice_filter(input_path, str(output_path))

        state_data = await state.get_data()
        send_to_user_id = int(state_data.get("user_id","0"))
        await state.clear()

        voice_file = FSInputFile(str(output_path))

        # Send sender his filtered voice
        await message.answer_voice(caption="<i>Голосове з фільтром:</i>", voice=voice_file, parse_mode="HTML")
        # send reciever voice message with effect
        await bot.send_voice(caption=message_anon("Голосове повідомлення"),chat_id=send_to_user_id, voice=voice_file,parse_mode="HTML", reply_markup=keyboard_anon_message(message.from_user.id))

        await message.answer(SENT_SUCCESS, reply_markup=keyboard_reply_menu())

    except Exception as e:
        print(str(e))
        await message.answer(SENT_FAILURE, reply_markup=keyboard_reply_menu())

    finally:
        if input_path:
            if os.path.exists(input_path):
                os.remove(input_path)
                #log here

        if output_path:
            if os.path.exists(output_path):
                os.remove(output_path)
                #log here also maybe idk
