require "TSLib"
require("common")
require("register")
require("createRole")
require("beginAccount")
require("playgame")
function main()
    init(1)
    setTable(H)
    Unit.State.Name = "init"
    -- Unit.State.Name="CcreateRole1"

    -- Unit.Param.CcreateRole1={
    --     account="dalaoban21",
    --     roleCount=1,
    --     totalCount=4,
    --     from="loginAccount"
    -- }

    showMessage("开始运行")
    while true do
        showMessage("当前状态:" .. tostring(Unit.State.Name))
        local nextState = processState(Unit.State, Unit.State.Name, Unit.Param[Unit.State.Name])
        showMessage("nextState:" .. nextState)
        if Unit.Param[nextState].retry ~= 1 and Unit.State.Name ~= "init" then
            Unit.Param[nextState].task = Unit.Param[Unit.State.Name].task
            Unit.Param[nextState].from = Unit.State.Name
        else
            -- 重置重试状态
            Unit.Param[nextState].retry = 0
        end
        Unit.State.Name = nextState
        mSleep(100)
    end
end
Unit.Param.Error = {
    errorType = "空",
    state = "空"
}
GLOBAL_TASK = {
    task = "beginAccount"
}

function Unit.State.Error(errorInfo)
    if errorInfo.errorType == "beginAccount" then
        stopSSApp()
        return errorInfo.task
    end

    if errorInfo.errorType == "create_error" then
        while true do
            showMessage("不能注册账号了")
            toast("不能注册账号了", 1)
            mSleep(5000)
        end
    end

    while true do
        showMessage("未处理的错误" .. errorInfo.errorType)
        stopSSApp()
        mSleep(5000)
        return "init"
    end
end

Unit.Param.init = {
    -- task="beginAccount", --createRole 创建角色，register --注册账号 -- regAndcreate注册并创建
    appType = APP_SS
}

function Unit.State.init(initParam)
    -- local task="register"
    -- local appType=APP_SS
    -- Unit.Param.beginTask.task="register"
    -- Unit.Param.beginTask.appType=APP_SS
    -- 单窗口单ip就不用了
    -- start_vpn()
    local task = "waitForLogin"
    local appType = APP_SS
    Unit.Param.beginTask.task = task
    Unit.Param.beginTask.appType = APP_SS
    writeFileString("/sdcard/touch_status.txt", "start\n")
    return "beginTask"
end

SERVER_ADDR = "http://192.168.0.103:5000"

-- function afterLogin()
--     XM.Print("等待账号")
--     XM.SetTableID("登录界面")
--     if Unit.Param.login.appType==APP_XM then

--         XM.Print("等待公告")

--         waitPic(602,74,677,118,"1")
--         XM.RndTap(644,607)
--         sleep(2000)
--         XM.RndTap(624,523)
--         sleep(5000)
--     else
--         XM.Print("等待上士登录页面")
--         if waitPic(600,396,678,439,5)==true then
--             XM.Print("找到上士登录按钮")
--         end

--     end

-- end
Unit.Param.beginTask = {
    appType = 2
}
function Unit.State.beginTask(taskInfo)
    -- 任务初始化
    return taskInfo.task
end
Unit.Param.loginAccount = {
    account = "dalaoban21",
    from = "createRole",
    qu = 109
}

function inputAccount(account)
    showMessage("开始输入账号:" .. account)
    randomTap(638, 281)
    for i = 0, #account, 1 do
        inputText(string.sub(account, i, i))
        rndSleep(300, 600)
    end
    touchDown(583, 583)

    rndSleep(500, 1000)
    touchUp(583, 583)
    randomTap(583, 387)
    rndSleep(1000, 2000)
    randomTap(800, 377)
    rndSleep(1000, 2000)

    for i = 0, #account, 1 do
        inputText(string.sub(account, i, i))
        rndSleep(300, 600)
    end
    randomTap(612, 486)
    showMessage("账号输入完毕")
end
function chosePlayArea()
    randomTap(617, 403)
    rndSleep(2000, 3000)
    for i = 1, 5, 1 do
        moveTo(656, 506, 657, 483)
        moveTo(657, 483, 656, 423)
        moveTo(656, 423, 657, 326)
        moveTo(657, 506, 662, 268)
    end
    --
    rndSleep(2000, 3000)
    touchDown(530, 609)
    rndSleep(2000, 3000)
    touchUp(530, 609)
    rndSleep(2000, 3000)
    randomTap(661, 515)
end

function Unit.State.loginAccount(accountInfo)
    if startToAccount() ~= true then
        Unit.Param.Error.errorType = "startError"
        Unit.Param.Error.name = "loginAccount"
        return "Error"
    end
    -- switchTSInputMethod(true);
    local account = accountInfo.account
    inputAccount(account)
    -- switchTSInputMethod(false);

    if waitPic1(755, 405, 806, 437, "ss_register_ok1.png", 5, 2) == true then
        randomTap(836, 163)
        randomTap(869, 161)
        rndSleep(3000, 4000)
    end
    if waitPic1(516, 81, 582, 119, "ss_register_ok.png", 5, 2) == true then
        randomTap(804, 610)
        rndSleep(1000, 2000)
    end
    if waitPic1(770, 586, 841, 626, "ss_yinlogin.png", 10, 3) == true then
        randomTap(804, 610)
        rndSleep(1000, 2000)
    end
    if waitPic1(770, 586, 841, 626, "ss_yinlogin.png", 10, 3) == true then
        randomTap(804, 610)
        rndSleep(1000, 2000)
    end
    if waitPic1(614, 77, 635, 94, "ss_gonggao.png", 10, 3) == true then
        randomTap(631, 595)
        rndSleep(1000, 2000)
    end
    if waitPic1(614, 77, 635, 94, "ss_gonggao.png", 10, 3) == true then
        randomTap(643, 606)
        rndSleep(1000, 2000)
    end
    -- 选区逻辑
    chosePlayArea()
    local success = false
    -- 排队
    -- if  waitPic1(1071,618,1088,643,"ss_loginpd_ok.png",10,1) then
    --     local cnt=0
    --     while waitPic1(1071,618,1088,643,"ss_loginpd_ok.png",10,1)==true do
    --         mSleep(10000)
    --         nLog("排队等待"..(cnt*20).."s")
    --         if cnt>3600/20 then
    --             nLog("排队超时,重新登录")
    --             stopSSApp()
    --             return "loginAccount"
    --         end
    --         if  waitPic1(551,4,639,52,"chose_user.png",2,1) then
    --             success=true
    --             nLog("角色选择页")
    --             break
    --         end
    --         if  success==false and waitPic1(951,71,987,92,"ss_role_create.png",2,1)  then
    --             success=true
    --             nLog("角色创建页面")
    --             break
    --         end

    --     end

    -- end
    mSleep(5000)
    local cnt = 0
    while cnt < 3600 / 5 do
        if waitPic1(551, 4, 639, 52, "chose_user.png", 2, 1) then
            success = true
            showMessage("角色选择页")
            break
        end
        if success == false and waitPic1(146, 12, 229, 55, "ss_role_create.png", 2, 1) then
            success = true
            showMessage("角色创建页面")
            break
        end
        -- 崩溃重启试试
        if appIsRunning(PACKAGES[APP_SS]) == 0 then
            showMessage("重启app")
            stopSSApp()
            accountInfo.retry = 1
            return "loginAccount"
        end

        cnt = cnt + 1
        mSleep(5000)
    end

    if accountInfo.from ~= nil and success then
        return accountInfo.from
    end
    Unit.Param.Error.errorType = "loginAccountError"
    Unit.Param.Error.name = "loginAccount"
    return "Error"
end
function main_test()
    init(1)
    -- tap(46,61)
    -- mSleep(3000)

    -- todo 配置默认编辑器
    -- randomTap(144, 959)
    -- mSleep(3000)
    -- randomTap(408, 1168)
    -- mSleep(10000)

    -- nLog(ret)
    -- randomTap(638,281)
    -- init(0)
    -- local account="zhuandaqian3233"
    -- local t=io.popen("curl http://192.168.0.103:5000 ")
    -- local a = t:read("*all")
    -- nLog(a)
    mSleep(10000)
end
function start_vpn()
    --必须使用雷电的默认文件选择器
    -- 修改文件名为wwwww_clash.yaml,保证配置文件在最后一个的位置
    init(0)
    showMessage("开始")
    runApp("com.github.kr328.clash")
    wait_begin()
    -- 停止已经启动的代理
    w1 = widget.find({["id"] = "com.github.kr328.clash:id/title", ["text"] = "代理"})
    if w1 ~= nil then
        nLog("点击a")
        randomTap(202, 330)
        mSleep(3000)
    end
    randomTap(202, 462)
    mSleep(3000)

    randomTap(630, 212)
    mSleep(3000)
    randomTap(140, 938)
    mSleep(3000)

    -- 选择最后一个文件作为代理
    randomTap(350, 600)
    for i = 1, 5 do
        moveTo(300, 1000, 300, 200, 200)
        mSleep(200)
    end
    mSleep(3000)
    randomTap(284, 1215)
    mSleep(2000)
    randomTap(638, 106)
    mSleep(2000)
    randomTap(54, 103)
    mSleep(1000)
    randomTap(419, 322)
    mSleep(1000)
    os.execute("input keyevent KEYCODE_HOME")
    init(1)
end

function wait_begin()
    while true do
        w2 = widget.find({["id"] = "com.github.kr328.clash:id/title", ["text"] = "配置"})
        if w2 ~= nil then
            showMessage("程序已经启动")
            widget.click(w2)
            break
        end
    end
end

-- main_test()
-- start_vpn()

--   nLog("???")
-- main_test()

main()

-- main()
