import os
import subprocess

import discord


async def download_video(message):
    async with message.channel.typing():
        url_src = next(url for url in message.content.split(" ") if "tiktok.com" in url)
        # Des fois ca fail alors on va test 3x
        attempt = 0
        while attempt < 3:
            download_process = subprocess.run(["youtube-dl", url_src, "-o", "tmp.%(ext)s"],
                                              capture_output=True, encoding='utf-8')
            if download_process.returncode == 0:
                try:
                    await message.reply(file=discord.File(r'tmp.mp4'))
                except:  # Si le fichier est trop gros...
                    await message.reply("Je dois compresser tout ca att 2 sec... "
                                               "(Je ne répondrai plus au commande le temps de la compression)")

                    compression_process = subprocess.run(["ffmpeg", "-i", "tmp.mp4", "-filter:v", "fps=30", "-crf",
                                                          "35", "tmp_comp.mp4"])
                    if compression_process.returncode == 0:
                        await message.channel.reply(file=discord.File(r'tmp_comp.mp4'))
                        os.remove("tmp_comp.mp4")
                os.remove("tmp.mp4")
                return
            else:
                attempt += 1
        await message.channel.send("J'ai pas réussi à recup la vidéo... Renvoie le lien pour que je retest..."
                                   " Sinon c'est que TikTok a changé un bail et qu'il faut un fix.")
