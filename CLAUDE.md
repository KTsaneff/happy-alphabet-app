# Весела азбука — приложение (БГ + EN)

Образователна игра за българчета в предучилищна възраст: учат **българската и/или английската азбука** по избор, с превключване с един клик. Наследник на [vesela-azbuka](https://github.com/KTsaneff/vesela-azbuka) (само БГ, уеб) — онова репо не се пипа оттук.

Цели: уеб версия (GitHub Pages) **и** Android приложение, публикувано в **Google Play**.

## Принципи

- **Един код за уеба и Android.** Цялата игра е в `docs/index.html`; Android е Capacitor обвивка около `docs/`.
- **Без сървър и без събиране на данни.** Напредъкът е в `localStorage` (ключ `happy-alphabet-v1`), всяко четене/писане в `try/catch`. Няма реклами, analytics, SDK-та на трети страни, идентификатори. Това е изискване на Google Play **Families Policy** — не добавяй нищо, което го нарушава.
- **Работи офлайн.** Шрифтовете (Rubik, Nunito, OFL) са вградени в `docs/fonts/`; няма външни заявки.
- **За 3–4-годишно дете:** огромни бутони, Таралежко (🦔) води и говори; детето не трябва да чете, за да играе.
- Интерфейсът за родителя и commit съобщенията са на **български**.

## Структура

| Път | Какво |
| --- | --- |
| `docs/index.html` | Играта: CSS, разметка, JS (един IIFE) |
| `docs/privacy.html` | Политика за поверителност БГ/EN (линк за Google Play) |
| `docs/sw.js`, `docs/manifest.webmanifest` | PWA и офлайн кеш само за уеба (в Android не се регистрира) |
| `docs/fonts/` | woff2 шрифтове + лицензи |
| `android/` | Capacitor 8 проект. Ръчно променени: `MainActivity.java` (цял екран), `app/build.gradle` (versionCode от CI, подписване), `res/values/styles.xml` (splash), иконите |
| `android/app/debug.keystore` | **Нарочно в git** — фиксиран тестов ключ (паролa `android`), за да се инсталират тестовите APK един върху друг |
| `tools/make_icons.py` | Генерира всички иконки и splash екрани (Pillow) |
| `capacitor.config.json` | `appId: com.ktsaneff.veselaazbuka` — **не се сменя след първото публикуване в Play** |
| `.github/workflows/android.yml` | CI билд |

## Как е устроена играта

- **Азбуки:** обект `PACKS` → `bg` (30 букви) и `en` (26). Ред: `[главна, малка, ДУМА, картинка, име за гласа, превод, rare, noPic]`. `rare` = не се ползва като дразнител (Ъ, Ь); `noPic` = не участва в „Коя картинка?“ (Ь). Персонализирани SVG: `STORK` (Щ), `XYLO` (X).
- **Езикът на подканите:** `TXT.bg` / `TXT.en`. При английската азбука родителят избира (`S.enPrompts`) дали Таралежко говори на български или английски. `say([[текст, език], …])` смесва езиците — напр. подкана на БГ + име на буквата на EN.
- **Говор:** в Android — `@capacitor-community/text-to-speech` (системния TTS); в браузъра — Web Speech API. Ако няма глас за даден език, частта се пропуска тихо; родителският панел показва статуса.
- **Състояние `S`:** `lang, voice, sfx, name, enPrompts` + `p.bg` / `p.en` — отделни `stars, stickers, set, seen, dipDate` за всяка азбука.
- **Сцени:** `home`, `learn`, `find`, `pic`, `balloons`; диплома след всички букви на азбуката; родителски панел ⚙️.
- **Android:** бутон Назад → `goBack()` (затваря прозорци / връща към началото / излиза); при `pause` спира говора и балоните.

## Билд и публикуване

- **Уеб:** GitHub Pages от `main` / `docs` (включва се ръчно в Settings → Pages) → `https://ktsaneff.github.io/happy-alphabet-app/`.
- **Android CI** (`android.yml`, при всеки push в `main`):
  1. `npm ci` → `npx cap sync android` → `./gradlew assembleDebug -PversionCode=<run_number>`
  2. Проверка на APK (aapt2 + apksigner) — резултатът е в описанието на release-а.
  3. Публикува APK като pre-release **`test-build`** → постоянен линк:
     `https://github.com/KTsaneff/happy-alphabet-app/releases/download/test-build/vesela-azbuka.apk`
  4. Ако има secrets `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD` → подписан `app-release.aab` (artifact) за Google Play.
- Локално: `npm ci`, `npx cap sync android`, после `cd android` и `./gradlew assembleDebug` (нужни JDK 21 и Android SDK).
- След промяна в `docs/` винаги `npx cap sync android` преди Android билд.

## Текущо състояние (19.10.2026)

- ✅ Уеб версията с двете азбуки работи; CI билдът минава; APK-то е валидно (aapt2/apksigner OK, minSdk 24, targetSdk 36).
- ⚠️ **Отворен проблем:** на Samsung таблет (One UI 8.5) тестовият APK дава „Приложението не е инсталирано“. Самият файл е проверен и е наред → вероятно блокира устройството: Samsung **Auto Blocker**, Play Protect, детски профил/Family Link. Чака се обратна връзка от собственика.
- ⏳ GitHub Pages за `docs/` още не е потвърдено включено.
- ⏳ **Google Play:** собственикът регистрира личен developer акаунт. Нов личен акаунт → нужен затворен тест с **12 тестери × 14 последователни дни** преди публикуване. Предстои: upload keystore + secrets, store listing (БГ/EN), скрийншоти, Data safety, Target audience (деца → Families), content rating.
- Идея за по-късно: записани аудио файлове вместо системен TTS (на някои устройства няма български глас).
