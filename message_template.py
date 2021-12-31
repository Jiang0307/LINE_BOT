feature = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.icon-icons.com/icons2/916/PNG/512/Menu_icon_icon-icons.com_71858.png",
    "size": "4xl",
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
        "margin": "md",
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "依照階級查詢",
                "size": "md",
                "color": "#555555",
                "flex": 2
              },
              {
                "type": "text",
                "text": "Search by tier",
                "size": "sm",
                "color": "#111111",
                "align": "start",
                "flex": 2
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "依照英雄查詢",
                "size": "md",
                "color": "#555555",
                "flex": 2
              },
              {
                "type": "text",
                "text": "Search by champion",
                "size": "sm",
                "color": "#111111",
                "align": "start",
                "flex": 2
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "依照對抗查詢",
                "size": "md",
                "color": "#555555",
                "flex": 2
              },
              {
                "type": "text",
                "text": "Search by matchup",
                "size": "sm",
                "color": "#111111",
                "align": "start",
                "flex": 2
              }
            ]
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
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