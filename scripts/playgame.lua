require("TSLib")
require("common")
require("tools")
-- 卡分解页面
MAP = {["格鲁"] = {321, 164}}
SUB_MAP = {
    ["悬空"] = {963, 292},
    ["暮光"] = {308, 610}
}
SUB_MAP1 = {
    ["悬空"] = {
        ["矿脉"] = {243, 610},
        {
            ["失落"] = {766, 607},
            ["龙族"] = {296, 486},
            ["幽暗"] = {710, 492},
            ["罪恶"] = {333, 366},
            ["天空"] = {689, 367}
        },
        ["宫殿"] = {707, 253},
        ["冰火"] = {280, 244}
    },
    ["暮光"] = {["灼热"] = {1104, 411}, ["幽寒"] = {535, 374}, ["黄昏"] = {775, 566}, ["恶毒"] = {491, 168}}
}
Unit.Param.playGamer = {
    ["taskRole"] = {
        {
            ["role"] = 1,
            ["副本"] = {"赫顿城", "暮光", "幽寒", "普通", 999, true},
            ["分解装备"] = {true, true, true, true},
            ["出售装备"] = {false, true, true, true}
        },
        {
            ["role"] = 2,
            ["副本"] = {"赫顿城", "暮光", "幽寒", "普通", 999, true},
            ["分解装备"] = {true, true, true, true},
            ["出售装备"] = {false, true, true, true}
        },
        {
            ["role"] = 3,
            ["副本"] = {"赫顿城", "暮光", "幽寒", "普通", 999, true},
            ["分解装备"] = {true, true, true, true},
            ["出售装备"] = {false, true, true, true}
        },
        {
            ["role"] = 4,
            ["副本"] = {"赫顿城", "暮光", "幽寒", "普通", 999, true},
            ["分解装备"] = {true, true, true, true},
            ["出售装备"] = {false, true, true, true}
        }
    },
    appType = APP_SS
}

function Unit.State.playGamer(taskInfo)
    showMessage("初始化刷副本的信息！")

    if taskInfo.from == "playGamerOne" then
        showMessage("执行完毕，退出脚本")
        writeFileString("/sdcard/touch_status.txt", "finish\n", "a")
        lua_exit()
    end
    if runAppWithoutLogin(APP_SS) ~= true then
        showMessage("启动游戏出错！")
        return "Error"
    end
    -- bid, _ = frontAppBid()

    -- if bid ~= PACKAGES[APP_SS] then
    --     if runAppWithoutLogin(APP_SS) ~= true then
    --         showMessage("启动游戏出错！")
    --         return "Error"
    --     end
    -- else
    --     showMessage("app is running")
    -- end
    -- showMessage(taskInfo.taskRole)
    if wait_bak() then
        showMessage("在主城中")
        goChoseGamer()
        SetTableID("上士登录页")
        if waitColor("角色选择", false, 30 * 60, 10) then
            showMessage("等待角色选择")
        end
    end
    showMessage("xxx")
    Unit.Param.playGamerOne = {
        taskRole = taskInfo.taskRole,
        cur = 1
    }
    return "playGamerOne"
    --   ret=get_num(544,280,584,307,"90ABB4-242926")
end
Unit.Param.waitForLogin = {
    taskRole = {},
    cur = 1
}
-- 等待登录进入游戏
function Unit.State.waitForLogin(taskInfo)
    if runAppWithoutLogin(APP_SS, true) ~= true then
        showMessage("启动游戏出错！")
        return "Error"
    end
    lua_exit()
end

Unit.Param.playGamerOne = {
    taskRole = {},
    cur = 1
}
function Unit.State.playGamerOne(taskInfo)
    showMessage("开始清日常")
    if taskInfo.cur > 1 then
        return "playGamer"
    end
    -- for key, value in pairs(taskInfo) do
    --     showMessage("key:" .. key)
    -- end
    mSleep(5000)
    role_info = taskInfo.taskRole[taskInfo.cur]
    -- showMessage(taskInfo.taskRole)
    local role_idx = role_info.role
    showMessage("role_idx" .. role_idx)
    local fb = role_info["副本"]
    local fj = role_info["分解装备"]
    local cs = role_info["出售装备"]
    -- nLogtab
    -- nLogTab(fj)
    --  nLogTab(cs)
    choseGamer(role_idx)
    randomTap(637, 666)
    mSleep(1000)
    closeGG()
    if role_idx == 1 then
        set_base_picture()
        mSleep(2000)
    end
    if fb[6] then
        doPalyOne(fb[1], fb[2], fb[3], fb[4], fb[5])
    end
    wait_bak()
    mSleep(1000)

    clear_package(fj, cs)
    mSleep(1000)
    goChoseGamer()
    SetTableID("上士登录页")
    if waitColor("角色选择", false, 30 * 60, 10) then
        showMessage("等待角色选择")
    end
    mSleep(1000)
    showMessage("cur role:" .. taskInfo.cur)
    taskInfo.cur = taskInfo.cur + 1
    return "playGamerOne"
end

function choseGamer(idx)
    showMessage("选角色")
    idx = idx - 1
    for i = 0, 5, 1 do
        randomTap(100, 346)
        mSleep(1000)
    end
    local page, other = math.modf(idx / 8)
    for i = 0, page - 1, 1 do
        randomTap(1184, 355)
        mSleep(1000)
    end
    idx = idx % 8
    local row, other1 = math.modf(idx / 4)
    local col = idx % 4
    local x = 276 + 225 * col
    local y = 292 + 219 * row
    showMessage("tap x:" .. x .. "y:" .. y)
    randomTap(x, y)
    mSleep(1000)
end
-- init(1)
-- choseGamer(8)

function goChoseGamer()
    showMessage("通过回城页面到选择色页面")
    -- 通过回城页面到选择色页面
    randomTap(32, 54)
    rndSleep(1000)
    randomTap(863, 604)
    rndSleep(1000)
    -- 等待页面稳定
end

function goMap(area, subarea, name, level)
    showMessage("走大地图")
    -- area 地图
    -- name 图名
    -- level 等级

    randomTap(1190, 100)
    for i = 0, 2, 1 do
        moveTo(734, 210, 711, 673)
        showMessage("滑动地图")
        rndSleep(100)
    end
    -- 其他地图
    SetTableID("进副本")
    local xy = SUB_MAP[subarea]

    for i = 1, 3 do
        showMessage("x:" .. xy[1] .. ",y:" .. xy[2])
        randomTap(xy[1], xy[2])
    end

    if waitColor("副本返回", false, 120, 3) ~= true then
        return false
    end
    xy = SUB_MAP1[subarea][name]
    showMessage(xy[1])
    showMessage(xy[2])
    randomTap(xy[1], xy[2])
    if waitColor("开始挑战", false, 15, 3) ~= true then
        return false
    end

    if level == "普通" then
        randomTap(673, 166)
    elseif level == "冒险" then
        randomTap(853, 156)
    elseif level == "勇士" then
        randomTap(985, 164)
    elseif level == "王者" then
        randomTap(1143, 162)
    end
    return true
end
function beginPlayOne(area, subarea, name, level)
    showMessage("进图")
    if goMap(area, subarea, name, level) ~= true then
        return false
    end
    mSleep(5000)
    local num = get_num(1142, 12, 1206, 54, "DBDEE0-111111|BFC5CB-111111")
    if num == nil or num <= 0 then
        showMessage("没精力了")
        randomTap(60, 25)
        mSleep(3000)
        randomTap(60, 25)
        mSleep(3000)
        randomTap(1232, 48)
        mSleep(5000)
        return false
    end
    randomTap(1095, 632)
    showMessage("开始挑战")
    return true
end

function doPalyOne(area, subarea, name, level, times)
    showMessage("开始单刷:" .. times .. "次")
    if beginPlayOne(area, subarea, name, level) ~= true then
        return false
    end
    cnt = 0
    local time_cost = 0
    local begin_time = os.time()
    has_check = false
    while true do
        if waitPlayBegin() then
            showMessage("副本开始了")
        end
        if has_check == false then
            if checkautoplay() == false then
                --完善一场状态
            else
                has_check = true
                showMessage("已经开始自动挂机")
            end
        end
        time_cost = os.time() - begin_time

        local is_end = false
        if waitPlayEnd() then
            is_end = true
        end
        showMessage("副本已经结束")
        if is_end then
            doOpenCard(true, true)
            cnt = cnt + 1
            showMessage("已经刷了xxx次")
            if cnt >= times then
                showMessage("副本刷完了")
                doRePalyOne(false)
                wait_bak()
                break
            else
                doRePalyOne(true)
                showMessage("继续副本")
            end
        end
        if multiColor({{918, 177, 0xddbb88}, {926, 187, 0xb79663}, {913, 195, 0xb18a54}, {932, 178, 0xc9aa7b}}) then
            randomsTap(918, 177)
        end
        if find(5, {"上士登录页", "拜师"}, true) then
            showMessage("关闭拜师")
        end
        if find("变强卡屏", 5, true) then
            showMessage("变强卡屏")
            return false
        end
        if find(5, {"登录广告", "精力"}, false) then
            showMessage("已经超时回城了")
            if beginPlayOne(area, subarea, name, level) ~= true then
                return false
            end
        end
    end
end
function wait_bak()
    -- 等待回城
    local cnt = 0
    while cnt < 3 do
        if find(5, {"登录广告", "精力"}, false) then
            return true
        end
        cnt = cnt + 1
        mSleep(1000)
    end
    return false
end

function checkautoplay()
    showMessage("检查自动挂机")
    SetTableID("进副本")
    cnt = 0
    while cnt < 100 do
        -- if find("自动副本", 5, false) then
        --     showMessage("已经自动挂机了")
        --     return true
        -- end
        if multiColor({{34, 268, 0xffd278}, {48, 268, 0xffffbb}, {40, 286, 0xffff67}, {27, 277, 0xffbb2a}}, 90, false) then
            showMessage("已经自动挂机了")
            return true
        end

        -- showMessage("检查次数" .. cnt)
        cnt = cnt + 1
        mSleep(200)
    end
    randomTap(42, 273)

    return false
end
function waitPlayBegin()
    showMessage("等待副本开始")
    SetTableID("进副本")
    cnt = 0
    while cnt < 30 do
        keepScreen(true)
        if
            multiColor(
                {
                    {85, 44, 0xb81313},
                    {86, 62, 0x18386d}
                }
            )
         then
            return true
        end
        keepScreen(false)
        cnt = cnt + 1
    end
    return false
end
function waitPlayEnd()
    showMessage("等待副本结束")
    SetTableID("进副本")

    if waitColor("选择卡牌", false, 3, 2) == true then
        showMessage("副本结束")
        return true
    end

    -- if multiColor({{529, 43, 0x101334}, {87, 37, 0x301630}, {1227, 84, 0xefde99}, {1188, 91, 0x3e3c30}}) then
    --     nLog("副本已经开始")
    --     return true
    -- end
    mSleep(2000)
    return false
end
function doOpenCard(card1, card2)
    showMessage("翻牌")
    local x, y = 226, 171
    local ret = getRnd(0, 3)
    x = x + 280 * ret
    if card1 then
        randomTap(x, y)
    end
    ret = getRnd(0, 3)

    x, y = 216, 568
    x = x + 280 * ret
    if card2 then
        randomTap(x, y)
    end
    randomTap(1208, 88)
    showMessage("翻牌完毕")
end
function closeSR()
    showMessage("关闭神秘商人")
    keepScreen(false)
    keepScreen(true)
    x, y =
        findMultiColorInRegionFuzzy(0xb59c73, "-4|26|0x685526,-4|17|0x08101f", 80, 1096, 636, 1096, 636, {orient = 2})
    if x ~= -1 then
        randomsTap(x, y)
    else
        showMessage("没有商人1")
    end
    keepScreen(false)
    mSleep(1000)
    keepScreen(true)
    if multiColor({{1113, 112, 0xe7cd90}, {1128, 125, 0xb4935f}, {1114, 130, 0xba9560}, {1128, 116, 0xc9ae84}}) then
        showMessage("点击商人2")
        randomsTap(1127, 126)
    else
        showMessage("没有商人2")
    end
    keepScreen(false)
    mSleep(1000)
    keepScreen(true)
    if
        (isColor(888, 75, 0xe9cd98, 85) and isColor(899, 86, 0xc6a677, 85) and isColor(912, 100, 0x9a703b, 85) and
            isColor(907, 80, 0xcbac7e, 85) and
            isColor(891, 97, 0xb48b57, 85))
     then
        showMessage("点击商人3")
        randomsTap(898, 85)
    else
        showMessage("没有商人3")
    end
    keepScreen(false)
    mSleep(1000)
end

function doRePalyOne(bool)
    showMessage("点击再来一次")
    local cnt = 0
    SetTableID("进副本")
    -- randomTap( 577,58)
    mSleep(2000)
    while true do
        closeSR()
        if multiColor({{1119, 37, 0xffffff}, {1126, 43, 0x89898c}, {1126, 46, 0x0b1030}, {1113, 45, 0x05081a}}) then
            if bool then
                showMessage("点继续")
                randomTap(1105, 147)
            else
                showMessage("点回城")
                randomTap(1100, 55)
            end
            return true
        end
        if find("图刷完了", 5, true) then
            showMessage("图刷完了，没疲劳了")
            return false
        end

        mSleep(200)
        cnt = cnt + 1
        if cnt >= 5 then
            showMessage("等待超时")
            return false
        end
    end
    showMessage("没有找到再次挑战！")
    return false
end
function wait_xm()
end
function wait_ss(xm)
    -- 等待上士登录账号
    showMessage("等待上士登录")
    SetTableID("上士登录页")
    while true do
        -- 登录页
        if find("登录按钮", true, 5) then
            mSleep(1000)
        end

        if find("绑定手机", true, 5) then
            mSleep(1000)
        end

        if find("公告", true, 5) then
            mSleep(1000)
        end
        if find("排队", false) then
            mSleep(1000)
        -- break
        end
        if find("登录人满", true) then
            -- nLog("人满了")
            mSleep(1000)
        -- break
        end

        if xm then
            if find("游戏登录按钮", false, 5) then
                mSleep(1000)
                dialogRet("手动选区", "选区", "", "", 0)
                xm = false
            end
        else
            -- 点击登录
            -- break
            if find("游戏登录按钮", true, 5) then
                mSleep(1000)
            end
        end
        if waitColor("角色选择", false, 10, 5) then
            showMessage("进入游戏成功")
            return true
        end
        mSleep(1000)
        -- nLog("??")
    end
    -- mSleep(5000)
    -- if find("排队", false) then
    --     nLog("排队")
    -- end

    showMessage("进入游戏超时")
    return false
end

function runAppWithoutLogin(appType, xm)
    if xm == nil then
        xm = false
    end

    showMessage("直接登录，不输入账号")
    if find(5, {"登录广告", "精力"}, false) then
        showMessage("已经登录")
        return true
    else
        stopSSApp()
    end
    local ret = runApp(PACKAGES[appType])
    if ret == 0 then
        if appType == APP_SS then
            return wait_ss(xm)
        elseif APP_SS == APP_XM then
            return wait_xm(xm)
        else
            return false
        end
    end
    return false
end

function closeGG()
    showMessage("关闭广告页")
    SetTableID("上士登录页")
    while true do
        if find("广告1", true) then
            showMessage("GG")
            mSleep(1000)
        end
        if find("广告2", true) then
            showMessage("GG")
            mSleep(1000)
        end
        if find("登录完成", true) then
            showMessage("GG")
            mSleep(1000)
            break
        end
        if find("决斗段位", true) then
            showMessage("GG")
            mSleep(1000)
            break
        end

        mSleep(1000)
    end
    showMessage("登录完成")
end
-- closeGG()
function get_email()
    showMessage("领邮件")
    SetTableID("上士登录页")
    has_email = false
    for i = 1, 100 do
        x, y =
            findMultiColorInRegionFuzzy(
            0x2f73ac,
            "-3|16|0xd90100,-3|31|0x0c2745,7|9|0xf2e3c9",
            90,
            412,
            350,
            499,
            625,
            {orient = 2}
        )

        if x ~= -1 then
            tap(x, y)
            has_email = true
            mSleep(1000)
            break
        else
            showMessage("kkkk")
        end
    end
    if has_email == false then
        return has_email
    end

    randomTap(95, 211)
    showMessage("邮箱不为空")

    randomTap(1026, 668)
    mSleep(500)

    randomTap(107, 121)
    mSleep(500)
    randomsTap(1033, 554)
    mSleep(500)
    randomTap(1130, 556)
    mSleep(500)

    randomTap(106, 300)
    mSleep(500)
    randomsTap(1033, 554)
    mSleep(500)
    randomTap(1130, 556)
    mSleep(500)

    randomTap(73, 22)
    mSleep(500)
    return has_email
end
function fenjiezb(type, a, b, c)
    if a == nil then
        a = true
    end
    if b == nil then
        b = true
    end
    if c == nil then
        c = false
    end
    SetTableID("分解装备")
    -- 分解装备
    -- 背包
    randomTap(1222, 672)
    mSleep(2000)
    if type == 1 then
        showMessage("分解")
        randomTap(861, 675)
        mSleep(1000)
    else
        showMessage("出售")
        randomTap(1041, 679)
        mSleep(1000)
    end
    x, y = findMultiColorInRegionFuzzy(0x6ed532, "", 80, 423, 399, 474, 440, {orient = 2})
    if (x == -1 and a) or (x ~= -1 and not a) then
        randomTap(449, 424)
        mSleep(1000)
    end
    x, y = findMultiColorInRegionFuzzy(0x6ed532, "", 80, 553, 399, 602, 442, {orient = 2})
    if (x == -1 and b) or (x ~= -1 and not b) then
        randomTap(573, 427)
        mSleep(1000)
    end
    x, y = findMultiColorInRegionFuzzy(0x6ed532, "", 80, 677, 396, 732, 439, {orient = 2})
    if (x == -1 and c) or (x ~= -1 and not c) then
        randomTap(700, 426)
        mSleep(1000)
    end
    randomTap(654, 519)
    mSleep(1000)
    if find("分解确认", 5, true) then
        showMessage("分解装备")
    end
    mSleep(1000)
    local finish = false
    if (isColor(640, 408, 0x104eb6, 80)) then
        showMessage("没有装备了")
        randomTap(640, 423)
        mSleep(1000)
        randomTap(453, 511)
        mSleep(1000)
        finish = true
    else
        mSleep(10000)
        randomTap(893, 154)
    end
    randomTap(57, 24)
    mSleep(5000)
    return finish
    -- if get_email() ~= true then
    --     break
    -- end
end
function clear_package(fj, cs)
    -- 清理邮件和分解装备
    for i = 1, 10 do
        if fj[1] ~= true and cs[1] ~= true then
            break
        end
        if fj[1] then
            showMessage("分解装备")
            if fenjiezb(1, fj[2], fj[3], fj[4]) == true then
                showMessage("没装备了")
            end
        end
        if cs[1] then
            showMessage("出售装备")
            if fenjiezb(2, cs[2], cs[3], cs[4]) == true then
                showMessage("没装备了")
            end
        end

        if get_email() ~= true then
            showMessage("没邮件了")
            break
        end
    end
end
function set_base_picture()
    randomsTap(46, 62)
    mSleep(1000)
    randomTap(241, 257)
    mSleep(2000)
    moveTo(628, 171, 628, 140)

    tap(653, 395)
    mSleep(500)
    tap(541, 535)
    mSleep(500)
    randomsTap(1116, 133)
    mSleep(1000)
end
init(1)
setTable(H)
SetTableID("上士登录页")
mSleep(5000)
-- set_base_picture()
-- SetTableID("进副本")
-- checkautoplay()
-- showMessage("xxx")
-- if find("变强卡屏", 5, true) then
--     showMessage("变强卡屏", 0, 700)

-- end
-- showTextView("变强卡屏","aa")

-- if find(5, {"上士登录页", "拜师"}, true) then
--     showMessage("关闭拜师")
-- end
-- randomTap(711,338)

-- setTable(H)
-- closeGG()
--   if multiColor({{918, 177, 0xddbb88}, {926, 187, 0xb79663}, {913, 195, 0xb18a54}, {932, 178, 0xc9aa7b}}) then
--             showMessage("月卡弹出？")
--             randomsTap(918, 177)
--   end
--     showMessage(string.format("0x%X",getColor(918, 177)))
-- todo 配置技能
-- init(1)
-- setTable(H)
-- waitPlayEnd()
-- for i = 1, 300 do
--     if find(5, {"登录广告", "精力"}, false) then
--         showMessage("已经超时回城了")
--     -- if beginPlayOne(area, subarea, name, level) ~= true then
--     -- end
--     end
-- end
-- -- if multiColor({{918, 177, 0xddbb88}, {926, 187, 0xb79663}, {913, 195, 0xb18a54}, {932, 178, 0xc9aa7b}}) then
--     randomsTap(918, 177)
-- end
-- if find(5, {"登录广告", "精力"}, false) then
--     showMessage("已经超时回城了")
--     if beginPlayOne(area, subarea, name, level) ~= true then
--         return false
--     end
-- end
-- fenjiezb(1,true,true,true)
-- mSleep(3000)

-- clear_package({true, true, true, true}, {false, true, true, true})
-- checkautoplay()
-- checkautoplay()
-- doPalyOne("赫顿城", "暮光", "幽寒", "普通", 3)
-- if multiColor({{529, 43, 0x101334}, {87, 37, 0x301630}, {1227, 84, 0xefde99}, {1188, 91, 0x3e3c30}}) then
--     showMessage("副本已经开始")
-- -- return true
-- end
-- setTable(H)
-- SetTableID("进副本")

-- init(1)
-- setTable(H)
--
