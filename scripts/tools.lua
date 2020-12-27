-- 一些通用函数和代码
require "TSLib"
--使用本函数库必须在脚本开头引用并将文件放到设备 lua 目录下

Unit = {
    State = {},
    Param = {}
}
SERVER_ADDR = "http://192.168.0.103:5000"
-- Param.state={
--     from="", 来源状态
--     task="", 当前正在执行的task
-- }
function waitFound(to, step, func)
    local cnt = 0
    while cnt < to do
        if func() then
            -- nLog("找到图色")
            return true
        end
        mSleep(step * 1000)
        cnt = cnt + step
    end
    return false
end
function processState(stateTable, stateName, stateParam)
    if stateTable[stateName] ~= nil then
        return stateTable[stateName](stateParam)
    end
    return "Error"
end
function waitPic11(x1, y1, x2, y2, picpath, to, step)
    to = to or 120
    step = step or 5
    nLog("找图" .. picpath)
    return waitFound(
        to,
        step,
        (function()
            local x, y = findImage(picpath, x1, y1, x2, y2)
            return x ~= -1 and y ~= -1
        end)
    )
end

function waitPic1(x1, y1, x2, y2, picpath, to, step)
    to = to or 120
    step = step or 5
    nLog("找图" .. picpath)
    return waitFound(
        to,
        step,
        (function()
            snapshot("/sdcard/tmp.png", x1, y1, x2, y2)
            local url = string.format("%s/compare_img1?target=%s", SERVER_ADDR, picpath)
            local command_str = string.format('curl -F "ocr_file=@/sdcard/tmp.png" "%s"', url)
            nLog("执行str：" .. command_str)
            local t = io.popen(command_str)
            local a = t:read("*all")
            return a == "True"
        end)
    )
end
function save_img(x1, y1, x2, y2, picpath)
    snapshot("/sdcard/tmp.png", x1, y1, x2, y2)
    local url = string.format("%s/save_img?target=%s", SERVER_ADDR, picpath)
    local command_str = string.format('curl -F "ocr_file=@/sdcard/tmp.png" "%s"', url)
    nLog("执行str：" .. command_str)
    local t = io.popen(command_str)
    local a = t:read("*all")
    return a == "True"
end
function get_num(x1, y1, x2, y2, colors)
    local status, iRet =
        pcall(
        function()
            local ret = snapshot("/sdcard/a1.png", x1, y1, x2, y2)
            local url = string.format("%s/upload1?colors=%s", SERVER_ADDR, colors)
            local command_str = string.format('curl -F "ocr_file=@/sdcard/a1.png" "%s"', url)
            nLog("执行str：" .. command_str)
            local t = io.popen(command_str)
            local a = t:read("*all")
            nLog("AA")
            return tonumber(a)
        end
    )
    if status == true then
        return iRet
    else
        nLog("脚本报错了")
        return nil
    end
end

function getRnd(a, b)
    math.randomseed(getRndNum()) -- 随机种子初始化真随机数
    num = math.random(a, b) -- 随机获取一个 1 - 100 之间的数字
    return num
end

function rndSleep(a, b)
    if b == nil then
        b = a + a / 2
    end
    math.randomseed(getRndNum()) -- 随机种子初始化真随机数
    num = math.random(a, b) -- 随机获取一个 1 - 100 之间的数字
    mSleep(num)
end
function wrapNextState(param, state)
    Unit.Param[param.next] = param.nextParam
    return param.next
end
Tools = {
    tab = nil,
    tabid = nil
}
function setTable(tab)
    Tools.tab = tab
end

function SetTableID(id)
    Tools.tabid = id
end
function nLogTab(tab)
    local content = ""
    for key, value in pairs(tab) do
        content = content .. key .. ":" .. tostring(value) .. ","
    end
    nLog("{" .. content .. "}")
end
function findm(colors, click, rnd)
    if rnd == nil then
        rnd = 5
    end

    -- nLogTab(colors)
    degree = math.ceil(colors[2] * 100)
    x1 = colors[3]
    y1 = colors[4]
    x2 = colors[5]
    y2 = colors[6]
    -- nLog("报错出："..find_id)
    mail_all = strSplit(colors[7], "-")

    posandcolor = string.gsub(colors[8], "-", "|")
    -- nLogTab({mail_all[1],posandcolor,degree,x1,y1,x2,y2})
    local table = {orient = 2}
    table["main"] = mail_all[2]
    if colors[10] ~= nil then
        table["list"] = colors[10]
    end

    keepScreen(true)
    local x, y = findMultiColorInRegionFuzzy(mail_all[1], posandcolor, degree, x1, y1, x2, y2, table)
    -- nLogArr({mail_all[1], posandcolor, degree, x1, y1, x2, y2, table})
    -- nLog("x:" .. x .. "y:" .. y)
    keepScreen(false)
    if x ~= -1 then
        if click then
            randomTap(x, y, rnd)
        end
        return true
    else
        return false
    end
end

function find(...)
    local Arr = {}
    local Rnd, id, click = 5, "", false
    if ... == nil then
        return false
    end
    Arr = {...}
    for i = 1, #Arr do
        if type(Arr[i]) == "string" or type(Arr[i]) == "table" then
            id = Arr[i]
        elseif type(Arr[i]) == "number" then
            Rnd = Arr[i]
        elseif type(Arr[i]) == "boolean" then
            click = Arr[i]
        end
    end
    find_tab = Tools.tab[Tools.tabid]
    find_id = nil
    -- nLog(id)
    if type(id) == "table" then
        -- nLog("here")
        find_tab = Tools.tab[id[1]]
        find_id = id[2]
    else
        find_id = id
    end
    -- nLog("图色id:" .. find_id)
    for i = 1, #find_tab do
        if find_tab[i][1] == find_id then
            nLog("取到色点数据：" .. find_id)
            colors = find_tab[i]
            if type(colors[2]) == "number" then
                return findm(colors, click, Rnd)
            elseif type(colors[2]) == "table" then
                keepScreen(true)
                local ret = multiColor(colors[2])
                keepScreen(false)
                -- nLog("是否点击"..tostring(click)..tostring(ret))
                if click and ret then
                    nLog("点击" .. find_id)
                    randomTap(colors[3][1], colors[3][2], Rnd)
                end
                return ret
            end
        end
    end

    return false
end

function waitColor(id, click, timeout, step)
    if timeout == nil then
        timeout = 5
    end
    if click == nil then
        click = false
    end
    if step == nil then
        step = 1
    end
    -- nLog(tostring(click))
    return waitFound(
        timeout,
        step,
        (function()
            -- nLog(tostring(id))
            -- nLog(tostring(click))
            local ret = find(5, id, click)
            return ret
        end)
    )
end

function tools_test()
    init(1)
    setTable(H)
    SetTableID("进副本")
    -- if find("副本返回") then
    --     nLog("测试成功")
    --     toast("测试成功",0.5)
    -- else
    --     nLog("测试失败")
    -- end
    -- waitColor("副本返回",true)
    -- local x,y= findMultiColorInRegionFuzzy(0x00ff00, "2|0|0x00ff00,0|-2|0x00ff00", 90, 92, 4, 105, 13)
    -- toast("找色成功x:"..x.."y:"..y)
end
-- tools_test()
function calc_ps(a, b)
    s, _ = string.find(a, "0x")
    if s ~= nil then
        a = string.sub(a, 3)
    end
    if b == nil then
        return "0x" .. a
    end
    s, _ = string.find(b, "0x")
    if s ~= nil then
        b = string.sub(b, 3)
    end
    r1 = tonumber("0x" .. string.sub(a, 1, 2))
    g1 = tonumber("0x" .. string.sub(a, 3, 4))
    b1 = tonumber("0x" .. string.sub(a, 5, 6))
    r2 = tonumber("0x" .. string.sub(b, 1, 2))
    g2 = tonumber("0x" .. string.sub(b, 3, 4))
    b2 = tonumber("0x" .. string.sub(b, 5, 6))
    a = string.format("0x%02X%02X%02X", math.max(0, r1 - r2), math.max(0, g1 - g2), math.max(0, b1 - b2))
    b = string.format("0x%02X%02X%02X", math.min(r1 + r2, 255), math.min(g1 + g2, 255), math.min(b1 + b2, 255))
    return a, b
end
function convert_color(color)
    mail_list = strSplit(color, "-")
    a = mail_list[1]
    b = mail_list[2]
    a, b = calc_ps(a, b)

    main = a
    if b ~= nil then
        main = main .. "-" .. b
    end
    return main
end
function wrap_str(str)
    return string.format('"%s"', str)
end

function nLogArr(arr)
    -- nLog("arr")
    outstr = ""
    for i = 1, #arr do
        outstr = outstr .. tostring(arr[i]) .. ","
    end
    nLog(string.format("{%s},", string.sub(outstr, 1, -2)))
end

function convert_tab(tab)
    -- 偏色格式也会转换
    for i = 1, #tab do
        color = tab[i]
        color[7] = wrap_str(convert_color(color[7]))
        local other_list = strSplit(color[8], ",")
        local new_other = ""
        for i = 1, #other_list do
            other = strSplit(other_list[i], "|")
            new_other = new_other .. other[1] .. "|" .. other[2] .. "|" .. convert_color(other[3]) .. ","
        end
        new_other = string.sub(new_other, 1, -2)
        color[1] = wrap_str(color[1])
        color[8] = wrap_str(new_other)
        nLogArr(color)
        mSleep(200)
    end
end
function showMessage(msg)
    showTextView(tostring(msg), "abc", 60, 679, 261, 703, "left", "eeeeee", "000000", 10, 1, 0.5, 0, 50)
end

-- H = {}
-- H["进副本"] = {
--     -- {"副本返回", 0.8, 14, 20, 55, 64, "0x243450",  "4|8|0xb4945f,-3|18|0x172438"},
--     -- {"副本返回",0.8,13,23,41,60,"0x13233F-0x354561","4|8|0x9F7F4B-0xC1A16D,-3|14|0x07152A-0x29374C"}
--     -- {"副本返回",0.8, 10, 25, 40, 55,"0x243450-0x111111","5|8|0xab8c58-0x111111,-5|10|0x1c2a41-0x111111"}

-- --   {"副本返回",0.8,12,33,42,62,"0x13233F-0x354561","4|8|0xA3834E-0xC5A570,-3|18|0x061327-0x283549"}
-- }
-- convert_tab(H["进副本"])
-- init(1)
-- setTable(H)
-- keepScreen(false)
-- keepScreen(true)
-- if find(5, {"进副本", "副本返回"}, false) then
--     nLog("测试成功")
-- else
--     -- if beginPlayOne(area, subarea, name, level) ~= true then
--     -- end
--     nLog("测试失败")
-- end
-- keepScreen(false)

-- nLog(tonumber("10")==10)
-- 将飞天XM格式转换位触动精灵
-- nLog(math.min(0,5))
-- a,b=calc_ps("0x000000","0x111111")
-- a,b=calc_ps("0xffffff","0x111111")
-- nLog(a)
-- nLog(b)
