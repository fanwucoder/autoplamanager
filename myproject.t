Unit={
State={},
Param={}
}
H={}
function processState(stateTable,stateName,stateParam)
    if stateTable[stateName]~=nil then
        return stateTable[stateName](stateParam)
    end
    return "Error"
end
H["登录界面"]={
{"上士登录按钮",0.9,603,399,625,422,"FFFFFF-111111","-4|2|FF6D2D-111111,0|5|FFFFFF-111111"},
{"登录按钮",0.8,608,588,682,631,"144393-000000","-7|-2|C7CDD7-000000,-15|6|CECECF-000000,13|-1|144495-000000"},
{"公告",0.8,600,77,681,117,"1A2942-000000","-2|-12|080C13-000000,-5|-11|FFFFFF-000000,6|-9|FFFFFF-000000"},
{"进入游戏",0.8,542,485,656,549,"FFFDF5-000000","-2|8|FDF6D6-000000,30|25|F98C41-000000,25|2|F75520-000000,40|14|FB7440-000000"},
{"进入游戏1",0.8,623,652,664,681,"9A2818-000000","0|10|9C3822-000000,0|14|EEDD99-000000,8|14|F3D298-000000"}
}


function afterLogin()
    XM.Print("等待账号")
    XM.SetTableID("登录界面")
    if Unit.Param.login.appType==APP_XM then
        
        XM.Print("等待公告")
        
        waitPic(602,74,677,118,"1")
        XM.RndTap(644,607)
        sleep(2000)
        XM.RndTap(624,523)
        sleep(5000)
    else
        XM.Print("等待上士登录页面")
        if waitPic(600,396,678,439,5)==true then
            XM.Print("找到上士登录按钮")
        end
        
    end
    
    
    --    XM.Print("开始寻找登录按钮")
    --    if waitFound(120,"公告",false)~=true then
    --        return "ERROR"
    --    end
    --    XM.Print("公告页面")
    --    if waitFound(120,"登录按钮",true)~=true then
    --        return "ERROR"
    --    end
    --    XM.Print("进入游戏页面")
    --    if waitFound(60,"进入游戏",true)~=true then
    --        return "ERROR"
    --    end
    --    XM.Print("角色选择页面")
    --    if waitFound(60,"进入游戏1",true)~=true then
    --        return "ERROR"
    --    end
    --    XM.Print("回城")
    
    
end

function choseGamer(idx)
    for i=0,2,1 do
        XM.RndTap(100,346)
        sleep(1000)
    end
    local page,other=math.modf(idx/8)
    for i=0,page-1,1 do
        XM.RndTap(1184,355)
        sleep(1000)
    end
    idx=idx %8
    local row,other1=math.modf(idx/4)
    local col=idx%4
    local x=276+225*col
    local y=292+219*row
    XM.RndTap(x,y)
    sleep(1000)
    
end
function goChoseGamer()
    -- 通过回城页面到选择色页面
    XM.RndTap(32,54)
    sleep(1000)
    XM.RndTap(863,604)
    sleep(1000)
    -- 等待页面稳定
    
end

function floatwinrun()
    -- 浮动窗口运行按钮执行的事件,如果不需要可去掉
    messagebox("脚本开始运行")
    require("XM")
    setrotatescreen(1)
    logopen()
    XM.AddTable(H)
    
    main()
    --    closeGg()
    --    goMap("赫顿城","悬空","矿脉","王者")
    --    doPalyOne("赫顿城","悬空","矿脉","王者",999)
    --    compare_img(1152,9,1193,56,3)
    
    --        XM.Print("自动游戏是否打开"..tostring(ret))
    --    local x=-1 y=-1 ret=-1
    --    x,y,ret=findmulticolor(1225,2,1279,67,"E1C193-111111","9|9|C0A070-111111,19|19|A07741-111111",0.9,0)
    --    if x~=-1 then
    --        tap(x,y)
    --    end
    --    XM.SetTableID("登录广告")
    --    if XM.Find(5,"活动广告",true) then
    --        XM.Print("ok!")    
    --    end
    
    --    cmd("su root ls /sdcard")
    --    sleep(2000)
    -- 公告
    --    get_text(600,73,680,122,"FFFFFF-111111|EFEFEF-111111|A2A2A2-111111")
    -- 角色等级
    --get_text(8,94,24,112,"EDEDEE-111111|ABA8AF-111111|E3E2E3-111111")
    --compare_img(602,74,677,118,"1")
    --    compare_img(554,498,641,536,2)
    --    sleep(10000)
    -- 进入游戏按钮，有可能被root字符串遮住
    --get_text(555,499,601,539,"FFEECC-101010|F8ECB0-101010|FFFFFf-222222|F9E8A4-444444")
    --    setrotatescreen(1)
    --    local t=cmdnew("curl http://www.baidu.com")
    --    XM.Print(t)
    --    main()
    --    goChoseGamer()
    --    choseGamer(0)
    --    choseGamer(4)
    --    choseGamer(7)
    --    choseGamer(8)
    
    --    local x=-1 y=-1 ret=-1
    --x,y,ret=findmulticolor(542,485,656,549,"FFFDF5-000000","-2|8|FDF6D6-000000,30|25|F98C41-000000,25|2|F75520-000000,40|14|FB7440-000000",0.8,0)
    --if x~=-1 then
    --tap(x,y)
    --end
    
    --    keepcapture(0) 
    --    local ret = screencap(0,0,500,500,"/sdcard/t.bmp")
    --    if ret == true then
    --        messagebox("截图成功")
    --    else
    --        messagebox("截图失败")
    --    end
    --    tap(633,609)
    --    sleep(100)
    
    
    
end
function main()
    
    Unit.State.Name="init"
    while true do
        Unit.State.Name=processState(Unit.State,Unit.State.Name,Unit.Param[Unit.State.Name])
        XM.Print("当前状态:"..tostring(Unit.State.Name))
        sleep(200)
    end
    
end
PACKAGES={"com.hegu.dnl.mi","com.hegu.dnl.sn79"}
-- appType类型
APP_XM=1 -- 小米
APP_SS=2 -- 上士
SERVER_ADDR="http://192.168.0.103:5000"
function startApp(appType)
    if appType==APP_XM then
        messagebox("启动小米版")
        local ret = cmd("su root am start -n com.hegu.dnl.mi/com.hegu.dnl.MainActivity") 
        return ret~=nil
    else
        local package=PACKAGES[appType]
        local ret=sysstartapp(package)
        XM.Print("RET:"..tostring(ret))
        return ret
    end
    
    
    return ret==1
    
end
function isRuning(appType)
    local ret=sysisrunning(PACKAGES[appType])
    return ret==1
end 
Unit.Param.init={
task="register",
appType=APP_SS 
}


function Unit.State.init(initParam)
    initParam.appType=APP_XM 
    Unit.Param.login.appType=APP_XM
    return initParam.task
end
Unit.Param.login={
appType=1,
next="choseUser"
}
function Unit.State.login(userInfo)
    XM.Print("登录")
    if startApp(userInfo.appType)   then
        afterLogin()
        Unit.Param.choseUser["cur"]=4
        return userInfo.next
    end
    
    return "Error"
    
end

Unit.Param.choseUser={
cur=0
}
H["登录广告"]={
{"活动广告",0.9,1225,2,1279,67,"E1C193-111111","9|9|C0A070-111111,19|19|A07741-111111"},
{"福利",0.9,1098,111,1145,161,"E8D18B-111111","9|10|C4A475-111111,21|21|A07842-111111"},
{"精力",0.9,97,17,128,43,"A9CC37-111111","-6|10|5D782C-111111"},
{"电池",0.9,87,0,120,15,"005A00-111111","4|6|005800-111111"}
}
function closeGg()
    
    XM.SetTableID("登录广告")
    for i=0,1000,1 do
        if XM.Find("电池") then
            break
        end
        if XM.Find("精力") then
            break
        end
        sleep(100)
    end
    for i=0,20,1 do
        if waitColor("活动广告",true,1)==true then
            XM.Print("关闭广告")
        end
        if waitColor("精力",false,1)==true then
            XM.Print("广告关完了")
            break
        end
        if waitColor("福利",true,1)==true then
            XM.Print("福利页面")
        end
        if waitColor("精力",false,1)==true then
            XM.Print("广告关完了")
            break
        end
    end
    
end
MAP={["格鲁"]={321,164}}
SUB_MAP={["悬空"]={963,292}}
SUB_MAP1={
["悬空"]={["矿脉"]={243,610}}
}
H["进副本"]={
{"副本返回",0.9,19,30,40,60,"273755-111111","7|9|BE9E6B-111111"},
{"开始挑战",0.9,1003,614,1022,648,"EDA314-111111","0|14|DA8C11-111111"},
{"血条",0.9,84,48,91,60,"B81512-111111","-3|10|193566-111111"},
{"未通关",0.9,27,261,52,290,"4C4C4C-111111","-3|14|D0D0D0-111111"},
{"选择卡牌",0.9,561,33,572,50,"141C43-111111","-2|4|FFFFFF-111111,-3|6|1B2549-111111"},
{"再来一次",0.9,1043,128,1051,139,"1F286E-111111","1|4|F2F2F5-111111,-1|8|172062-111111"},
{"神秘商人",0.9,1067,619,1088,654,"09101F-111111","1|5|CCAB72-111111,-2|8|0D1320-111111"},
{"神秘商人1",1097,92,1124,125,"101A28-111111","0|6|95724C-111111,-2|15|101A28-111111"},
{"神秘商人2",0.9,875,64,891,82,"101A28-111111","-1|4|ECCBA5-111111,-5|7|101A28-111111"},

}

function goMap(area,subarea,name,level)
    -- area 地图
    -- name 图名
    -- level 等级
    
    XM.RndTap(1190,100)
    for i=0,5,1 do
        XM.Swipe(734,210,711,673)
        sleep(600)
    end
    -- 其他地图
    XM.SetTableID("进副本")
    local xy=SUB_MAP[subarea]
    XM.RndTap(xy[1],xy[2])
    if waitColor("副本返回",false,120,3)~=true then
        return false
    end
    xy=SUB_MAP1[subarea][name]
    XM.Print(xy[1])
    XM.Print(xy[2])
    XM.RndTap(xy[1],xy[2])
    if waitColor("开始挑战",false,15,3)~=true then
        return false
    end
    if level=="普通" then
        XM.RndTap(673,166)
    elseif level=="冒险" then
        XM.RndTap(853,156)
    elseif level=="勇士" then
        XM.RndTap(985,164)
    elseif level=="王者" then
        XM.RndTap(1143,162)
    end
    return true
end
function beginPlayOne(area,subarea,name,level)
    if goMap(area,subarea,name,level)~=true then
        return false
    end
    XM.RndTap(1095,632)
    XM.Print("开始挑战")
    return true
end
function doPalyOne(area,subarea,name,level,times)
    
    if beginPlayOne(area,subarea,name,level)~=true then
        return false
    end
    cnt=0
    while true do
        local time_cost=0
        while waitPlayBegin()~=true do
            time_cost=time_cost+5
        end
        if cnt==0 then
            if checkautoplay()==false then
                --完善一场状态
                messagebox("游戏未通关该图")
                return false
            end
        end
        
        while waitPlayEnd()~=true do
            time_cost=time_cost+5
            
        end
        XM.Print("副本已经结束")
        doOpenCard(true,true)
        cnt=cnt+1
        if cnt>=times then
            doRePalyOne(false)
            break
        else
            doRePalyOne(true)
        end
        
        if XM.Find(5,{"登录广告","精力"},false) then
            XM.Print("已经超时回城了")
            if beginPlayOne(area,subarea,name,level)~=true then
                return false
            end
        end
    end
    
    
    
end
function checkautoplay()
    if compare_img(30,261,52,292,2)==true then
        if XM.Find("未通关",false) then
            return false
        else
            
            XM.RndTap(35,273)
        end
        
        return true
    end
    
    return true
end
function waitPlayBegin()
    XM.SetTableID("进副本")
    if waitColor("血条",false,5,1)~=true then
        return false
    end
    XM.Print("等待副本开始")
    return true
end
function waitPlayEnd()
    XM.SetTableID("进副本")
    
    if waitColor("选择卡牌",false,5,1)~=true then
        return false
    end
    XM.Print("等待副本结束")
    return true
end
function doOpenCard(card1,card2)
    local x,y=226,171
    local ret=rnd(0,3)
    x=x+280*ret
    if card1 then
        XM.RndTap(x,y)
    end
    ret=rnd(0,3)
    
    x,y=216,568
    x=x+280*ret
    if card2 then
        XM.RndTap(x,y)
    end
    XM.RndTap(1208,88)
    XM.Print("翻牌完毕")
end
function doRePalyOne(bool)
    local cnt=0
    while true do
        if XM.Find(5,"再来一次",false) then
            if bool then
                XM.RndTap(1124,137)
            else
                XM.RndTap(1124,137)
            end
            
            XM.Print("点击再次挑战")
            break
        end
        if XM.Find(5,{"进副本","神秘商人"},true) then
            XM.Print("关闭神秘商人") 
        end
        if XM.Find(5,{"进副本","神秘商人1"},true) then
            XM.Print("关闭神秘商人") 
        end
        if XM.Find(5,{"进副本","神秘商人2"},true) then
            XM.Print("关闭神秘商人") 
        end
        sleep(200)
        cnt=cnt+1
        if cnt>=100 then
            XM.Print("等待超时")
            return false
        end
    end
    XM.Print("没有找到再次挑战！")
    return false
end
function Unit.State.choseUser(choseUser)
    XM.Print("开始选择角色")
    choseGamer(choseUser.cur)
    XM.RndTap(638,666)
    sleep(1000)
    
    closeGg()
    return "finishPlayer"
end
Unit.Param.finishPlayer={
player_areas={
{area="赫顿城",
subarea="悬空",
name="矿脉",
level="王者",
times=999}
}
}
function Unit.State.finishPlayer(player)
    for i = 1, #player.player_areas do 
        palyer_info=player.player_areas[i]
        doPalyOne(palyer_info.area,palyer_info.subarea,
        palyer_info.name,palyer_info.level,palyer_info.times)
    end 
    doDouniu()
    doGebulin()
    doPata()
    clear_package()
    seezp()
    --    XM.Print(#player.player_areas)
    return "Error"
end
function doDouniu()
    -- 斗牛
end
function doGebulin()
    -- 哥布林
end
function doPata()
    -- 扫塔
end

function sendFrined()
    -- 好友赠送
end
function everyDay()
    -- 领每日，领在线，领日常
end
function clear_package()
    -- 清背包
end
function seezp()
    -- 查看珍品
end
function doQianghua()
    -- 做强化任务
end
function doDianzi()
    --做垫子
end
function saleDianzi()
    -- 上架垫子
end


