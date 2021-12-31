feature = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/lFq9NTg.jpg",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "介紹與說明",
              "text": "功能介紹與說明"
            },
            "height": "md",
            "color": "#ff9900",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/V2tkpQb.png",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "即時查詢",
              "text": "查詢即時匯率"
            },
            "height": "md",
            "color": "#ff6666",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/nQaCDXh.png",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "近期趨勢圖",
              "text": "查詢趨勢走向"
            },
            "height": "md",
            "color": "#ff66b3",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    },
    {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://i.imgur.com/UrSkoW4.png",
        "size": "full",
        "aspectMode": "fit",
        "aspectRatio": "1.25:1"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "推薦與否",
              "text": "是否推薦兌幣"
            },
            "height": "md",
            "color": "#b366ff",
            "style": "primary"
          }
        ],
        "spacing": "lg"
      }
    }
  ]
}
#============================================================================================
service = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.icon-icons.com/icons2/916/PNG/512/Menu_icon_icon-icons.com_71858.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "offsetTop": "xxl"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "OPTIONS",
        "weight": "bold",
        "size": "3xl",
        "align": "center",
        "offsetEnd": "none",
        "offsetStart": "none",
        "offsetBottom": "md"
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "下載圖片",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 3
          },
          {
            "type": "text",
            "text": "Download Image",
            "wrap": True,
            "color": "#666666",
            "size": "sm",
            "flex": 5
          }
        ],
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "英雄數據",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 3
          },
          {
            "type": "text",
            "text": "Champion Statistics",
            "wrap": True,
            "color": "#666666",
            "size": "sm",
            "flex": 5
          }
        ],
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "英雄故事",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 3
          },
          {
            "type": "text",
            "text": "Champion Story",
            "wrap": True,
            "color": "#666666",
            "size": "sm",
            "flex": 5
          }
        ],
        "margin": "sm"
      }
    ],
    "offsetBottom": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
#============================================================================================
info = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.icon-icons.com/icons2/916/PNG/512/Menu_icon_icon-icons.com_71858.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "offsetTop": "xxl"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "OPTIONS",
        "weight": "bold",
        "size": "3xl",
        "align": "center",
        "offsetEnd": "none",
        "offsetStart": "none",
        "offsetBottom": "md"
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "勝率",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 3
          },
          {
            "type": "text",
            "text": "Win rate",
            "wrap": True,
            "color": "#666666",
            "size": "sm",
            "flex": 5
          }
        ],
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "baseline",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "選取率",
            "color": "#aaaaaa",
            "size": "sm",
            "flex": 3
          },
          {
            "type": "text",
            "text": "Pick rate",
            "wrap": True,
            "color": "#666666",
            "size": "sm",
            "flex": 5
          }
        ],
        "margin": "sm"
      }
    ],
    "offsetBottom": "none"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}