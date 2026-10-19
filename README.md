# Весела азбука

Игра за деца в предучилищна възраст за учене на **българската** и **английската** азбука. Родителят избира азбуката с един клик; в английския режим Таралежко може да подканва на български или на английски.

- **Уеб версия:** `docs/` — статичен сайт, публикуван с GitHub Pages.
- **Android приложение:** `android/` — Capacitor обвивка около същия код; работи изцяло офлайн.
- **Без събиране на данни:** напредъкът се пази само на устройството. Виж [`docs/privacy.html`](docs/privacy.html).

## Структура

| Път | Какво има |
| --- | --- |
| `docs/index.html` | Цялата игра: азбуки, мини-игри, звездички, стикери, диплома |
| `docs/fonts/` | Шрифтове Rubik и Nunito (SIL Open Font License) — вградени, за да работи офлайн |
| `docs/privacy.html` | Политика за поверителност (BG/EN) за Google Play |
| `android/` | Android проект (Capacitor 8) |
| `tools/make_icons.py` | Генерира иконите и splash екраните |
| `.github/workflows/android.yml` | Компилира APK за тест и подписан AAB за Google Play |

## Как се добавя дума или буква

Азбуките са в `docs/index.html`, в обекта `PACKS`. Всеки ред е `[главна, малка, ДУМА, картинка, име на буквата за гласа, превод]`.

## Локален билд

```bash
npm ci
npx cap sync android
cd android && ./gradlew assembleDebug
```

## Подписване за Google Play

Workflow-ът създава подписан `app-release.aab`, когато в репото има тези secrets:

| Secret | Стойност |
| --- | --- |
| `ANDROID_KEYSTORE_BASE64` | upload keystore (`.jks`), кодиран с base64 |
| `ANDROID_KEYSTORE_PASSWORD` | парола на keystore-а |
| `ANDROID_KEY_ALIAS` | alias на ключа |
| `ANDROID_KEY_PASSWORD` | парола на ключа |

Без тях се строи само тестовият APK.
