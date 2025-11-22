# Brand Website URLs Reference

This file lists all the official website URLs for smartphone brands included in DialSmart.

## Priority Brands (Required)

| Brand | Official Website URL |
|-------|---------------------|
| Apple | https://www.apple.com |
| Asus | https://www.asus.com |
| Google | https://store.google.com |
| Honor | https://www.hihonor.com |
| Huawei | https://www.huawei.com |
| Infinix | https://www.infinixmobility.com |
| Oppo | https://www.oppo.com |
| Poco | https://www.poco.net |
| Realme | https://www.realme.com |
| Redmi | https://www.mi.com/redmi |
| Samsung | https://www.samsung.com |
| Vivo | https://www.vivo.com |
| Xiaomi | https://www.mi.com |

## Additional Brands

| Brand | Official Website URL |
|-------|---------------------|
| OnePlus | https://www.oneplus.com |
| Nokia | https://www.nokia.com |
| Motorola | https://www.motorola.com |
| Sony | https://www.sony.com |
| LG | https://www.lg.com |
| Lenovo | https://www.lenovo.com |
| HTC | https://www.htc.com |
| BlackBerry | https://www.blackberry.com |
| Tecno | https://www.tecno-mobile.com |

## Adding Custom Brands

To add a brand URL manually via SQL*Plus:

```sql
UPDATE brands SET website_url = 'https://www.example.com' WHERE name = 'BrandName';
COMMIT;
```

Or via the Admin Panel:
1. Go to http://192.168.0.178:5000/admin/brands
2. Click "Edit" on the brand
3. Enter the URL in "Official Website URL" field
4. Save

## Notes

- All URLs use HTTPS for security
- URLs open in a new tab when clicked
- Brand names are case-insensitive in the SQL updates (using UPPER())
- If a brand doesn't have a website_url, the brand name will display as plain text (not clickable)
