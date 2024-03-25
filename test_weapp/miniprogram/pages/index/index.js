// index.js
const app = getApp()


Page({
  data: {
    name: "Snow",
    user_name: "",
    user_xsxh: "",
    isNeedSubmit: true,
    latitude: null,
    longitude: null,
    qrcode: '',
    infoList: [],
    myinfo: ""
  },
  nameChange: function (e) {
    this.setData({
        user_name: e.detail.value
    });
  },
  xsxhChange: function (e) {
    this.setData({
        user_xsxh: e.detail.value
    });
  },
  onLoad() {
    wx.cloud.callContainer({
        "config": {
            "env": "prod-6g9pojl827ff5fd7"
        },
        "path": "/v1/check",
        "header": {
            "X-WX-SERVICE": "demo"
        },
        "method": "POST",
        "data": "",
        success: (res) => {
            console.log(res.data);
            if (res.data.code == "0")
            {
                this.setData({
                    isNeedSubmit: false,
                    user_name: res.data.name,
                    user_xsxh: res.data.xsxh
                });

            }

        }
    })
  },
  onButtonClick: function () {
    console.log("注册");
    
    wx.cloud.callContainer({
        "config": {
          "env": "prod-6g9pojl827ff5fd7"
        },
        "path": "/v1/create",
        "header": {
          "X-WX-SERVICE": "demo"
        },
        "method": "POST",
        "data": {
            "name": this.data.user_name,
            "xsxh": this.data.user_xsxh
        },
        success: (res) => {
            if(res.data.code == "0")
            {
                wx.showToast({
                    title: '注册成功',
                    icon: 'success',
                    duration: 2000
                  });
                this.setData({
                    isNeedSubmit: false
                });
            }
        }
      })
  },
  submit: function () {
    wx.cloud.callContainer({
        "config": {
          "env": "prod-6g9pojl827ff5fd7"
        },
        "path": "/v1/sign",
        "header": {
          "X-WX-SERVICE": "demo"
        },
        "method": "POST",
        "data": {
            "name": this.data.user_name,
            "xsxh": this.data.user_xsxh,
            "data": this.data.qrcode,
            "location": this.data.longitude + "," + this.data.latitude
        },
        success: (res) => {
            if(res.data.code == "0")
            {
                wx.showToast({
                    title: '签到成功',
                    icon: 'success',
                    duration: 2000
                  });
            }
        }
      })
  },
  ShowAll: function() {
    wx.cloud.callContainer({
        "config": {
          "env": "prod-6g9pojl827ff5fd7"
        },
        "path": "/v1/getall",
        "header": {
          "X-WX-SERVICE": "demo"
        },
        "method": "POST",
        "data": {

        },
        success: (res) => {
            this.setData({
                infoList: res.data
            })
        }
      })
  },
  ScanClick: function() {
    //   console.log("扫码");
    wx.getLocation({
        type: 'wgs84',
        success: (res) => {
          const latitude = res.latitude.toFixed(2).toString()
          const longitude = res.longitude.toFixed(2).toString()
          this.setData({
            latitude: latitude,
            longitude: longitude
          })
          
        },
        fail(err) {
            wx.showToast({
                title: '获取地理位置失败，请检查是否开启定位服务',
                icon: 'none',
                duration: 2000
            });
        }
    });  
    wx.scanCode({
        success: (res) => {
            const qrcodeData = res.result;
            this.setData({
                qrcode: qrcodeData
            });
            this.submit();
        }
        });
      
      

  },
  testauto: function(){
    wx.cloud.callContainer({
        "config": {
          "env": "prod-6g9pojl827ff5fd7"
        },
        "path": "/v1/auto_test",
        "header": {
          "X-WX-SERVICE": "demo"
        },
        "method": "GET",
        "data": {},
        success: (res) => {
            if(res.data.code == "0")
            {
                this.setData({
                    myinfo: res.data.debug
                })
            }
        }
      })
  }

})

