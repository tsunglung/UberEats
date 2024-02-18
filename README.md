<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant support for Uber Eats

[The readme in Traditional Chinese](https://github.com/tsunglung/UberEats/blob/master/README_zh-Hant.md).

***User the integration by your own risk***

## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/UberEats` > Category: Integration

Or manually copy `uber_eats` folder to `custom_components` folder in your config folder.

Then restart HA.

# Setup

You need to grab one cookie. If your get problem with https_result is 500, you need to get new cookie. (Temporary Solution, the cookie will be expirated after one month)

**1. Basic steps for grabbing**

1. Open the development tools (use Google chrome/Microsoft Edge) [Crtl+Shift+I / F12]
2. Open the Application tab, find "Storage"
3. Open the [Uber Eats Web site](https://www.ubereats.com/), Login your account.
4. Search for "sid" (for me only one itemes shows up, choose the first one)
5. copy the cookie like "QA....=" in the field "Value"  (mark with a mouse and copy to clipboard)

# Config

![grabbing](grabbing.png)

**2. Please use the config flow of Home Assistant**


1. With GUI. Configuration > Integration > Add Integration > Uber Eats
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter the account and cookie.
3. All fields are Required.

# Notice
The cookie will expired after days. If you saw the https_result is 403, you need get the new cookie again.
Then got to Configuration > Integration > Uber Eats > Options, enter the info of cookie.

Buy me a Coffee

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/UberEats/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/UberEats/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/UberEats/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |
