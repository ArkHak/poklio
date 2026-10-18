<p align="right"><a href="README.md">Русский</a> · <b>English</b></p>

<p align="center">
  <img src="images/hero-en.png" alt="Poklio — your libraries, your reader" width="100%">
</p>

<h3 align="center">Books from your subscription, on your PocketBook. Over Wi-Fi, no computer needed.</h3>

<p align="center">
  <a href="https://github.com/ArkHak/poklio/releases/latest"><img src="https://img.shields.io/github/v/release/ArkHak/poklio?label=download&style=for-the-badge&color=526B50" alt="Download"></a>
  &nbsp;
  <a href="#get-started"><img src="https://img.shields.io/badge/get_started-3_steps-202420?style=for-the-badge" alt="Get started"></a>
</p>

<p align="center">
  <img src="images/demo-en.gif" alt="What Poklio looks like" width="400">
</p>

## Why Poklio

<table>
  <tr>
    <td width="33%" valign="top">
      <b>Your whole library on your reader</b><br>
      The books in your Yandex Books account, with covers, right on your PocketBook.
    </td>
    <td width="33%" valign="top">
      <b>One tap to get a book</b><br>
      Tap Get book and it's in your reader's library, ready to open in the built-in reader app.
    </td>
    <td width="33%" valign="top">
      <b>Catalog search</b><br>
      Find a new book and add it to My books without reaching for your phone.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <b>Sign in with your phone</b><br>
      Scan a QR code and type your password on your phone, not on an on-screen keyboard.
    </td>
    <td valign="top">
      <b>Made for E Ink</b><br>
      Big buttons, page-turn keys and a color theme on Era Color.
    </td>
    <td valign="top">
      <b>Updates over Wi-Fi</b><br>
      A new version installs only when you tap Update. Interface in English and Russian.
    </td>
  </tr>
</table>

<p align="center">
  <img src="images/screens-en.png" alt="My books, a book card and signing in with a phone" width="100%">
  <br><sub>Screenshots. Books and covers are examples. Titles and descriptions come from the library catalog, so they stay in Russian.</sub>
</p>

## Get started

<table>
  <tr>
    <td width="33%" valign="top">
      <b>1. Install</b><br>
      Download <code>poklio.app.bin</code> from the <a href="https://github.com/ArkHak/poklio/releases/latest">latest release</a>, rename it to <code>poklio.app</code> and copy it to the <code>applications</code> folder on your reader over USB.
    </td>
    <td width="33%" valign="top">
      <b>2. Connect</b><br>
      In Poklio, tap Connect a library → Sign in with phone. Scan the QR code and sign in to Yandex.
    </td>
    <td width="33%" valign="top">
      <b>3. Read</b><br>
      Pick a book in My books, tap Get book, then Open.
    </td>
  </tr>
</table>

You'll need a Yandex Books account with a subscription and Wi-Fi, with your phone and reader on the same network.

<details>
<summary><b>Signing in with your phone, step by step</b></summary>

1. On the reader: Connect a library → Sign in with phone. A QR code appears.
2. Point your phone's camera at it and open the page.
3. Tap Sign in to Yandex and sign in to your account.
4. You'll land on a page saying that authorization in the Bookmate app failed. That's expected. Copy the page's full address: press and hold the address bar → Copy.
5. Go back to the Poklio tab, paste the address and tap Connect. My books opens on your reader.
</details>

<details>
<summary><b>Installing from a Mac</b></summary>

Finder adds a hidden helper file to the reader, which shows up as an extra item in Applications. Copy the file in Terminal instead (`PB700K3` is your reader's name in Finder):

```bash
cp -X ~/Downloads/poklio.app /Volumes/PB700K3/applications/
```

If the extra item is already there, delete `applications/._poklio.app` from the reader.
</details>

<details>
<summary><b>Backup sign-in, using a computer</b></summary>

1. On your computer, open [this link](https://oauth.yandex.ru/authorize?response_type=token&client_id=4483e97bab6e486a9822973109a14d05) and sign in to Yandex.
2. On the page saying that authorization in the Bookmate app failed, copy the full address.
3. Save it to a text file named `yandex.token` and copy it to the `poklio` folder on your reader over USB (the folder appears after you first open Poklio).
4. Open Poklio. It connects the library and deletes the file.

The file gives access to your account: don't share it, and delete it from your computer.
</details>

## Security

<table>
  <tr>
    <td width="50%" valign="top">
      <b>What's protected</b>
      <ul>
        <li>You type your password only on the Yandex website. The reader never sees it.</li>
        <li>Your sign-in data is encrypted over Wi-Fi and stored encrypted on the reader.</li>
        <li>The sign-in page only works while the sign-in screen is open, for up to 10 minutes.</li>
        <li>The reader won't install an update without the author's valid signature.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <b>What you should do</b>
      <ul>
        <li>After signing in, delete the Yandex page from your browser history and copy some other text.</li>
        <li>Sign in on your own network, not a public one.</li>
        <li>Protection on the reader guards against stray copies of its memory, not against someone holding the reader itself. If you lose your reader or give it away, revoke access in <a href="https://id.yandex.ru/personal/data-access">Yandex ID → Data access</a>.</li>
      </ul>
    </td>
  </tr>
</table>

## FAQ

<details>
<summary><b>Is this an official Yandex or PocketBook app?</b></summary>

No. Poklio is an independent project, not affiliated with PocketBook, Yandex or any other company. Service names are used only to show compatibility. Poklio connects to Yandex Books unofficially, so the connection is marked as experimental: if the service changes something, Poklio may stop working until an update.
</details>

<details>
<summary><b>Can I get a book that isn't in my subscription?</b></summary>

No. Poklio only gets books your account can read in full, and it doesn't bypass service restrictions.
</details>

<details>
<summary><b>Which readers does it work on?</b></summary>

It's tested on PocketBook 700 Era Color. It may work on other PocketBook models but hasn't been tested yet. [Let us know](https://github.com/ArkHak/poklio/issues) if you try.
</details>

<details>
<summary><b>Which libraries are supported?</b></summary>

Yandex Books for now (experimental). Litres, WB Books and others may come later.
</details>

<details>
<summary><b>Where are books stored, and how do I delete them?</b></summary>

In the `Books/Poklio` folder, so they show up in your PocketBook library. Delete file from device on the book card removes the file; the book stays in your Yandex Books library.
</details>

<details>
<summary><b>How do updates work?</b></summary>

Once a day, when Wi-Fi is on, Poklio checks for a new version. If there is one, the menu shows "New version available": tap Update, then close and reopen Poklio. Your books, sign-in and settings stay. You can turn off automatic checks in Settings.

If the new version won't start, connect the reader over USB and copy `system/state/poklio/update/poklio.app.prev` to the `applications` folder as `poklio.app` to get the previous version back.
</details>

<details>
<summary><b>Known limitations</b></summary>

- The PocketBook library picks up changes with a delay: a new book usually shows up there only after you restart the reader, and a deleted one stays in the list, unopenable, until a restart. Poklio itself shows changes right away.
- Book titles and descriptions are in the catalog's language, even with the English interface.
- On the lock screen, covers of books from Poklio are slightly cropped at the top and bottom.
</details>

<details>
<summary><b>Found a bug?</b></summary>

[Open an issue](https://github.com/ArkHak/poklio/issues) with your reader model, firmware version, Poklio version (Settings → About) and what happened. A log helps: turn on Diagnostic log in Settings, repeat the problem and attach `poklio/poklio.log` from the reader. It contains no passwords or sign-in data.
</details>

---

<p align="center">
  <sub>
    Poklio is an independent project, distributed under the <a href="LICENSE.md">license agreement</a>.<br>
    Share a link to this page so everyone gets the latest tested version.
  </sub>
</p>
