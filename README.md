# ru-direct geosite

`geosite.dat` dùng cho Xray / V2Ray gồm các domain Nga nên cho đi **DIRECT** (ngân hàng, chính phủ, dịch vụ công, mua sắm, mạng xã hội, nhà mạng...). Mỗi ngày tự build lại lúc 03:00 UTC.

Nguồn: [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) `category-ru` + [runetfreedom](https://github.com/runetfreedom/russia-v2ray-rules-dat) `ru-available-only-inside` + một ít bổ sung tay.

## Tải

```
https://github.com/huzgnm/ru-direct/releases/latest/download/geosite.dat
```

## Các mục

| Mục | Nội dung |
|---|---|
| `ru-direct` | Tất cả (gồm TLD) — dùng cái này |
| `ru-direct-notld` | Chỉ domain không đuôi Nga |
| `ru-tld` | `.ru .su .рф .рус .moscow .tatar ...` |
| `ru-bank` | Ngân hàng, tài chính |
| `ru-gov` | Chính phủ, dịch vụ công |
| `ru-medicine` | Y tế |
| `ru-shop` | Mua sắm, bán lẻ |
| `ru-social` | Yandex, VK, Mail.ru, OK, Rutube |
| `ru-telecom` | Nhà mạng |
| `ru-media` | Báo chí, giải trí |
| `ru-travel` | Du lịch, giao thông |
| `ru-edu` | Giáo dục |
| `ru-other` | Công ty Nga khác |

## Xray

Đặt file là `ru.dat` cạnh `xray` (hoặc trong `XRAY_LOCATION_ASSET`):

```json
{"type": "field", "domain": ["ext:ru.dat:ru-direct"], "outboundTag": "direct"}
```

Bản text: [`ru-direct.txt`](ru-direct.txt). Danh sách nguồn từng mục ở [`data/`](data).
