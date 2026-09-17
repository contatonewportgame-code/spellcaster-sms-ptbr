===============================================================================
                     SPELLCASTER (SEGA MASTER SYSTEM)
         BRAZILIAN PORTUGUESE 100% TRANSLATION & HISTORICAL RESTORATION
===============================================================================
Author & Chief Engineer: Cristiano Mariano
Brand / Label: Newportgame — Retro Game Preservation & Localization
Release Date: 2026
Target Platform: Sega Master System / Sega Mark III
===============================================================================

-------------------------------------------------------------------------------
📖 1. ABOUT THE PROJECT
-------------------------------------------------------------------------------
SpellCaster (known in Japan as Kujaku Ō / 孔雀王) is one of the most ambitious 
and technically impressive titles on the Sega Master System, seamlessly merging 
first-person graphic adventure, fast-paced action-platforming, and Japanese mythology.

This Brazilian Portuguese release was built entirely from the ground up using 
advanced low-level reverse engineering, cleanly reconstructing the ROM while 
strictly respecting Sega's factory hardware architecture (Z80 & VDP).

Project Highlights:
* 100% Story & Dialogue Translated: All 478 text boxes fully translated into 
  Portuguese, covering the entire journey (including the emotional scene with 
  the warrior Regina, the Ameno Spaceship, Mount Minakami, and the descent into Yomotsu).
* Full Diacritics System (11 Accents + Native Hyphen): Engineered via a hybrid 
  injection methodology utilizing 1bpp text memory and Sega's native 4BPP 
  Planar RLE compressed graphics blocks without overflowing shared VRAM.
* 100% Adventure Menus & Submenus Adapted: All 88 interaction options strictly 
  calibrated to the console's 8+8 character boundary limit (zero truncations).
* 100% Native HUD without Trampolines: The forest and pause scoreboards ("VIDA 20", 
  "ENER 20", "ATAQ", and "DEFS") were drawn directly into native video tables 
  without unstable Assembly hooks or stack trampolines (zero crash risk).
* Pixel Art Scenery Restoration (Yakisoba): The original Japanese sign in Izumo 
  Village was decompressed, repainted in pixel art, and recompressed using Sega's 
  canonical Planar RLE format with positive slack.
* Historical Restoration: Restored 10 crucial narrative dialogue pages and 
  final battle tutorial screens (<FC>) that were amputated by Sega of America in 1989.
* Factory Bug Extermination: Fixed the infamous debug stub "??07D??" left behind 
  by Sega QA at the Summit Temple, replacing it with the canonical text "NADA PARA PEGAR AQUI.".
* Cinematic Ending & Staff Credits: Fully localized end-credits sequence featuring 
  restored double-line spacing and sealed with the official signature at the opening:
  "VERSÃO BR: CRISTIANO MARIANO - NEWPORTGAME".

-------------------------------------------------------------------------------
💿 2. ROM SPECIFICATIONS & PATCH FILE
-------------------------------------------------------------------------------
* Patch File: SpellCaster (PT-BR) [Newportgame].ips
* Patch Format: Standard IPS (International Specification)

Recommended Base ROM (No-Intro Standard):
* File Name: SpellCaster (USA, Europe).sms
* File Size: 524,288 bytes (512 KB / 4 Megabits exact)
* Base ROM CRC32: 36729ED7

-------------------------------------------------------------------------------
🛠️ 3. HOW TO APPLY THE PATCH (.IPS)
-------------------------------------------------------------------------------
On Desktop (Windows / Linux / macOS):
1. Download Lunar IPS (LIPS) or Floating IPS (Flips).
2. Click "Apply IPS Patch".
3. Select "SpellCaster (PT-BR) [Newportgame].ips".
4. Select your clean, headerless "SpellCaster (USA, Europe).sms" ROM.
5. The patched Brazilian Portuguese ROM is ready to play!

In Your Web Browser (No installation required - Mobile / PC):
1. Visit: https://www.marcrobledo.com/RomPatcher.js/
2. In "ROM file", upload your clean "SpellCaster (USA, Europe).sms" ROM.
3. In "Patch file", upload the "SpellCaster (PT-BR) [Newportgame].ips" file.
4. Click "Apply patch" to download your localized ROM.

-------------------------------------------------------------------------------
🕹️ 4. COMPATIBILITY & TESTING
-------------------------------------------------------------------------------
Recommended Emulators:
* Desktop: Emulicious (Highly recommended - cycle-accurate SMS emulation), 
  RetroArch (Genesis Plus GX or Gearsystem cores), Kega Fusion, or BlastEm.
* Mobile (Android): RetroArch, Nostalgia.GG, or MD.emu.

On Real Hardware:
* 100% compatible with Master System I, II, III (Tec Toy) and original 
  Japanese/US hardware (Master System / Sega Mark III) via flash cartridges 
  (Everdrive / Master Everdrive / Mega Everdrive).
* Fully compatible with both 60 Hz (NTSC) and 50 Hz (PAL) video refresh rates.
* Dual Audio Support: Native support for standard PSG sound and orchestrations 
  via the Yamaha FM Sound Unit (YM2413).

-------------------------------------------------------------------------------
☕ 5. SUPPORT THIS AND FUTURE PROJECTS (VOLUNTARY DONATION)
-------------------------------------------------------------------------------
This project is 100% FREE and was developed purely out of passion for video game 
preservation and the rich historical legacy of the Sega Master System.

Countless late nights were invested in low-level Z80 disassembly, VRAM mapping, 
graphics decompression, and meticulous editorial localization.

If you enjoyed playing this translation on your emulator or real console and 
would like to support the author or buy him a coffee, voluntary contributions 
via Pix or PayPal are deeply appreciated:

* Pix (E-mail): contato.newportgame@gmail.com
* Account Holder: Cristiano Mariano
* Description: Retro Translation Donation / Newportgame

-------------------------------------------------------------------------------
📬 6. CONTACT & REVERSE ENGINEERING REPOSITORY
-------------------------------------------------------------------------------
* Official Contact: contato.newportgame@gmail.com
* Newportgame — Preservation, ROM Hacking, and Classic Game Localization

💻 For Developers & Researchers: The complete low-level documentation 
(The Master System Compendium, Forensic Memory Protocols) and the full Python 
forensic toolkit are openly available for study in the official Newportgame 
GitHub repository.

Thank you for playing and keeping the 8-bit Sega legacy alive!
===============================================================================

-------------------------------------------------------------------------------
📋 APPENDIX: UNIVERSAL CHARACTER TABLE (SpellCaster.tbl)
-------------------------------------------------------------------------------
Save the following content as "SpellCaster.tbl" to view or edit the ROM's 
script in classic hex viewers (WindHex, CrystalTile2, etc.):

00= 
01=!
07='
08=-
0A=Ô
0B=Ú
0C=[COMMA]
0D=[TAG0D]
0E=[PAUSE]
0F=Í
10=[TAG10]
11=[TAG11]
12=[TAG12]
13=[TAG13]
14=[TAG14]
16=[TAG16]
18=[TAG18]
1A=[SPEAKER]
1B=Õ
1C=[QUOTE1]
1D=Â
1E=[QUOTE2]
1F=?
20=Ã
21=A
22=B
23=C
24=D
25=E
26=F
27=G
28=H
29=I
2A=J
2B=K
2C=L
2D=M
2E=N
2F=O
30=P
31=Q
32=R
33=S
34=T
35=U
36=V
37=W
38=X
39=Y
3A=Z
3B=Á
3C=Ç
3D=Ó
3E=É
43=Ê
FC FF=[END]
FD=[LINE]
===============================================================================