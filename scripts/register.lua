require("common")
accounts_template={"dayigui","dalaoban","zhuandaqian","zhiduanda","haojixing","fwqkwhui","dayibkrj"}
name_tempale={"平易近人a", "宽宏大度", "冰清玉洁", "持之以恒", "锲而不舍", "废寝忘食", "大义凛然", 
    "临危不俱", "光明磊落", "不屈不挠", "鞠躬尽瘁", "死而后已", "料事如神", "足智多谋", 
    "融会贯通", "学贯中西", "博古通今", "才华横溢", "出类拔萃", "博大精深", "集思广益", "举一反三",
    "憨态可掬", "文质彬彬", "风度翩翩", "相貌堂堂", "落落大方  斗志昂扬", "意气风发", "威风凛凛",
    "容光焕发", "神采奕奕", "悠然自得", "眉飞色舞", "喜笑颜开", "神采奕奕", "欣喜若狂", "呆若木鸡", 
    "喜出望外", "垂头丧气", "无动于衷", "勃然大怒", "能说会道", "巧舌如簧", "能言善辩", "滔滔不绝", 
    "伶牙俐齿", "出口成章", "语惊四座", "娓娓而谈", "妙语连珠", "口若悬河", "三顾茅庐", "铁杵成针",
    "望梅止渴", "完璧归赵", "四面楚歌  ", "负荆请罪", "精忠报国", "手不释卷", "悬梁刺股", "凿壁偷光"}
account_idx=0
name_idx=0
Unit.Param.register={}
function Unit.State.register(accountInfo)
    nLog("执行注册账号")
    local tp_index=0
    local accout_tp=""
    local account=""

    if account_idx<5 then
        tp_index =math.random(1,7)
        accout_tp =accounts_template[tp_index]
        account=accout_tp..math.random(1,9999)
        Unit.Param.RcreateOneUser.account=account
        -- create_account(account)
        -- account_idx=account_idx+1
        return "RcreateOneUser"
    end

    --    RcreateUserFull()
    return "register"
end
Unit.Param.RcreateOneUser={}

function Unit.State.RcreateOneUser(userInfo)
    local account=userInfo.account
    nLog("开始注册账号:"..account)
    if startSS()~=true then
        Unit.Param.Error.errorType="startError"
        Unit.Param.Error.name="RcreateOneUser"
        return "Error"
    end
    if waitPic1(391,331,520,382,"ss_fisrt_login.png",5,1) then
        nLog("账号首次登录启动app成功")
        randomTap(815,408)
    else
        randomTap(788,502)      
    end
  
        
    rndSleep(300,600)
    randomTap(817,421)
    rndSleep(300,600)
    randomTap(787,549)
    rndSleep(300,600)
    randomTap(461,285)
    for i=0,#account,1 do
        inputText(string.sub(account,i,i))
        rndSleep(300,600)
    end
    randomTap(599,388)
    rndSleep(300,600)
    for i=0,#account,1 do
        inputText(string.sub(account,i,i))
        rndSleep(300,600)
    end
    randomTap(634,484)
    local success=false
  
    if waitPic1(755,405,806,437,"ss_register_ok1.png",5,1)==true    then 
        success=true
    elseif waitPic1(516,81,582,119,"ss_register_ok.png",5,1)==true then
        success=true
    
    end
    
    if success~=true then
        -- ip限制或者设备上限了
        Unit.Param.Error.errorType="create_error"
        Unit.Param.Error.name="RcreateOneUser"
        return "Error"
    end
    
    writeFileString("/sdcard/password.txt",""..account.."="..account,"a",1)
    nLog("注册账号成功："..account)
    stopSSApp()
    -- lua_exit()
    -- nLog("xxx")
    return "register"
end
