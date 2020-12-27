require("TSLib")
-- FINISH_PATH="/sdcard/finish.txt"
-- ACCOUNT_PATH="/sdcard/allPasswords.txt"
FINISH_PATH=userPath().."/res/finish.txt"
ACCOUNT_PATH=userPath().."/res/allPasswords.txt"
Unit.Param.createRole={
}

function Unit.State.createRole(taskInfo)
    
   
 
 
    if taskInfo.from=="CcreateRole1" then
        nLog("角色创建完毕")
        cur_cnt=cur_cnt+1
        writeFileString(FINISH_PATH,tostring(cur_cnt),"w")
        -- 创建角色完毕返回调用任务
        return taskInfo.task
    end
    nLog("设置账号，创建角色!")
    local accounts=readFileString(ACCOUNT_PATH)
    local tb_account=strSplit(accounts,"\n")
    -- local cur_cnt=readFileString(FINISH_PATH) or 1
    local cur_cnt=1
    cur_cnt=tonumber(cur_cnt)
    if cur_cnt>#tb_account then
        lua_exit()
        nLog("角色创建完毕")
    end
  
    account=strSplit(tb_account[cur_cnt],"=")[1]
    Unit.Param.CcreateRole1={
        account=account,
        roleCount=1,
        totalCount=4,
    }
    return "CcreateRole1"
end

Unit.Param.CcreateRole1={
    account="",
    roleCount=1,
    totalCount=4,
    from=""
}


function Unit.State.CcreateRole1(accountInfo)
    nLog("创建账号："..accountInfo.account)
    nLog("创建角色："..accountInfo.roleCount)
    if accountInfo.from=="loginAccount" then
        return "CcreateJob"
    end
    if accountInfo.from=="CcreateJob" then
        accountInfo.roleCount=accountInfo.roleCount+1
    end
    if  accountInfo.roleCount> accountInfo.totalCount then
        Unit.Param.createRole.from="CcreateRole1"
        return "createRole"
    end
    
    Unit.Param.loginAccount={
        account=accountInfo.account,
        from="CcreateRole1",
        qu=109,
    }
    return "loginAccount"
end


Unit.Param.CcreateJob={
    roleCount=4,
    account="" 
}

name_tempale={ "宽宏大度", "冰清玉洁", "持之以恒", "锲而不舍", "废寝忘食", "大义凛然", 
    "临危不俱", "光明磊落", "不屈不挠", "鞠躬尽瘁", "死而后已", "料事如神", "足智多谋", 
    "融会贯通", "学贯中西", "博古通今", "才华横溢", "出类拔萃", "博大精深", "集思广益", "举一反三",
    "憨态可掬", "文质彬彬", "风度翩翩", "相貌堂堂", "落落大方  斗志昂扬", "意气风发", "威风凛凛",
    "容光焕发", "神采奕奕", "悠然自得", "眉飞色舞", "喜笑颜开", "神采奕奕", "欣喜若狂", "呆若木鸡", 
    "喜出望外", "垂头丧气", "无动于衷", "勃然大怒", "能说会道", "巧舌如簧", "能言善辩", "滔滔不绝", 
    "伶牙俐齿", "出口成章", "语惊四座", "娓娓而谈", "妙语连珠", "口若悬河", "三顾茅庐", "铁杵成针",
    "望梅止渴", "完璧归赵", "四面楚歌  ", "负荆请罪", "精忠报国", "手不释卷", "悬梁刺股"}
ROLE_TYPE={
    {146,137,903,431},
    {146,137,1011,432},
    {146,137,1101,431},
    {146,137,906,488},
    {140,361,903,431},
    {139,444,1101,431}

}
function Unit.State.CcreateJob(accountInfo)
    nLog("开始创建角色")
    if  waitPic1(551,4,639,52,"chose_user.png",5,1) then 
        randomTap(1094,664)
        rndSleep(2000,3000)
        nLog("角色选择页")
    end
    -- 随机角色
    local zy=math.random(1,5)
    local p=ROLE_TYPE[zy]
    randomTap(p[1],p[2])
    rndSleep(2000,3000)
    randomTap(p[3],p[4])
    rndSleep(2000,3000)
    
    -- 生成名字
    local base=math.random(1,60)
    local base1=math.random(1,60)
    local roleName=name_tempale[base]..base1
    -- local roleName="凿壁偷光42"
    randomTap(999,576)
    rndSleep(2000,3000)
    inputText(roleName)
    rndSleep(300,600)
    randomTap(1244,650)
    rndSleep(2000,3000)
    randomTap(1009,651)
    rndSleep(3000,5000)
    randomTap(1145,658)
    rndSleep(3000,5000)
    -- 创建成功
    -- 退出app
    if   waitPic1(611,410,678,446,"name_error.png",5,1) then
        randomTap(636,425)
        rndSleep(3000,5000)
        randomTap(57,29)
        rndSleep(3000,5000)
        return "CcreateJob"
        
    end
    
    if waitPic1(1071,618,1088,643,"ss_role_create_ok.png",10,1)==true then
        nLog("角色创建成功")
        stopSSApp()
    else 
       
        Unit.Param.Error.errorType="CcreateJobError"
        Unit.Param.Error.name="CcreateJob"
        return "Error"

    end
    Unit.Param.CcreateRole1.from="CcreateJob"
 
    return "CcreateRole1"
    -- 回到角色创建
end
