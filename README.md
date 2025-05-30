# 青龙`openAPI`

## 一些缩写介绍：



id：青龙应用的client_id 2.11版本之后的青龙openapi，把_id改成了id

secret：青龙应用的client_secret

token:通过id和secret请求得到的用于身份验证的东西

URL:代表http://ip:5700，在这里我代指青龙的地址，新版的端口应该是5600

### 请求token:



方法：get，

请求参数：client_id、client_secret

示例：

```
const {data:{data:{token}}}=await axios.get(URL+'/open/auth/token',{params:{client_id:ID,client_secret:SECRET}})
```



`ps`：此后的请求都要携带请求头，可以全局设置在`axios`里，也可以每次请求携带。

### 添加ck：



方法：post，

参数：name,value,remarks。对应JD_COOKIE,ck的值，备注。备注的值可以为空

-示例：

```
const {data:{data:[{_id},...res]}}=await axios.post(URL+'/open/envs',[{name,value,remarks}],{headers:{Authorization:"Bearer "+token}})
```



`ps`：参数需要以数组形式传递，否则格式验证出错。这里的_id是青龙返回的，用于后面的请求携带

### 更新ck：



方法：put

参数：

示例：

```
const {data:res}=await axios.put(URL+'/open/envs',{
    name,
    value,
    remarks,
    _id},{
    headers:{
        Authorization:"Bearer "+token
    }
})
```



`ps`：这里的_id即相当于某个ck的身份证，需要更新某条ck就要传递它的身份证

### 删除ck：



方法：delete

参数：_id，需要删除的ck的id

示例：

```
const {data:res}=await axios({
        url:URL+'/open/envs',
        method:'delete',
        data:[_id],
        headers:{Authorization:"Bearer "+token}
})
```

### 根据id值获取完整ck信息：

方法：get

参数：_id，参数直接拼接在`url`里面

示例:

```
const {data:{data:{value,status,remarks=''}}}=await axios({
        url:URL+'/open/envs/'+_id,
        method:'get',
        headers:{Authorization:"Bearer "+token}
})
```



`ps`:`remarks`可为空，避免报错设置一个默认值。value是ck值。status是ck的状态，用1和0表示启用和禁用。原本的返回值内容更加丰富，我这里只解构三个相对实用的信息。

### 获取所有ck信息：



方法：get

参数：可不填

示例:

```
const{data:{data}}=await axios({
    url:URL+"/open/envs",
    method:'get',
    headers:{"Authorization":"Bearer "+token}
})
```



`ps`：返回值是一个数组。由于环境变量中可能存在其他不是JD_COOKIE的变量，可以过滤出数组中`name`位JD_COOKIE的值

```
data.filter(item=>item.name=="JD_COOKIE")
```
