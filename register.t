accounts_template={"dayigui","dalaoban","zhuandaqian","zhiduanda","haojixing","fwqkwhui","dayibkrj",""}
name_tempale={ "宽宏大度", "冰清玉洁", "持之以恒", "锲而不舍", "废寝忘食", "大义凛然", 
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
    local base_idx=20
    local total_account=5
    local tp_index=0
    local accout_tp=""
    local account=""
    local idx=0
    
    --    for i=1,6,1 do
    --        create_user(i)
    --        sleep(rnd(3000,5000))
    --        doSkipFlow()
    --        break
    --    end
    
    --    doSkipFlow()
    --    if waitPic(1105,31,1139,69,7,20,5)      then
    --                touchdown(218,574,9999)
    --                sleep(5000)
    --                touchup(9999) 
    --                for i=1,10,1 do
    --                    XM.RndTap(1175,650)
    --                    sleep(rnd(100,200))
    --                end
    --        XM.Print("房间1")
    --    end
    --    waitPic( 1136,33,1168,68,8,20,5)
    ---- 房间二
    --    waitPic( 1142,40,1171,69,9,20,5)
    ---- 后跳
    --    XM.RndTap(1214,538)
    --    if waitPic( 1141,325,1269,408,10,20,5) then
    --        XM.Print("完成房间2")
    --    end
    --副本结束逻辑
    
    
    
    -- 副本结束后跳过
    --    doSkipFlow()
    --XM.RndTap(136,235)
    --sleep(rnd(100,200))
    --for i=0,5,1 do
    --    XM.RndTap(168,521)
    --    sleep(rnd(100,200))
    --end
    -- 跳到选择页面
    --    goChoseGamer()
    --    sleep(1000*2)
    --    -- 打卡角色选择
    
    --    XM.RndTap(1113,666)
    
    local last_num=XM.ReadFile("/sdcard/anount_idx.txt")
    if last_num~=nil then
        account_idx=tonumber(last_num)+1
    end
    
    while account_idx<10 do
        tp_index =math.floor(account_idx/total_account)
        accout_tp =accounts_template[tp_index+1]
        idx=base_idx+account_idx%total_account
        account=accout_tp..idx
        create_account(account)
        account_idx=account_idx+1
        
    end
    --    RcreateUserFull()
    return "Rfinish"
    
end
Unit.Param.Rfinish={}
function Unit.State.Rfinish(param)
    sleep(1000)
end

function create_account(account)
    Unit.Param.login={
    appType=APP_SS,
    next="waitCreate"
    }
    XM.Print("创建账号:"..tostring(account))
    if Unit.State.login(Unit.Param.login)=="waitCreate" then
        XM.RndTap(788,502)
        
        sleep(rnd(300,600))
        XM.RndTap(817,421)
        sleep(rnd(300,600))
        XM.RndTap(787,549)
        sleep(rnd(300,600))
        XM.RndTap(461,285)
        for i=0,#account,1 do
            inputtext(string.sub(account,i,i))
            sleep(rnd(300,600))
        end
        XM.RndTap(599,388)
        sleep(rnd(300,600))
        for i=0,#account,1 do
            inputtext(string.sub(account,i,i))
            sleep(rnd(300,600))
        end
        XM.RndTap(634,484)
        sleep(rnd(10000,20000))
        
        --        XM.RndTap(892,164)
        --        sleep(rnd(5000,8000))
        --        
        --        XM.RndTap(812,607)
        --        sleep(rnd(1000,2000))
        --        XM.RndTap(812,607)
        --        sleep(rnd(3000,4000))
        --        XM.RndTap(644,605)
        --        sleep(rnd(3000,4000))
        --        XM.Print("账号创建完毕")
        if waitPic(854,127,911,183,11)==true            then
            
            XM.WriteFile("/sdcard/password.txt",""..account.."="..account.."\n")
            XM.WriteFile("/sdcard/anount_idx.txt",account_idx,true)
            messagebox("文件处理完毕")
        else
           while true do
                messagebox("注册失败了")
                sleep(1000)
           end
        end
        
        RquitApp()
        
    end
    
    return "login"
end
function Rxuanqu()
    -- 选区
    XM.RndTap(631,402)
    sleep(rnd(2000,3000))
    for i=0,5,1 do
        XM.Swipe(682,710,661,299)
        sleep(rnd(300,600))
    end
    XM.RndTap(562,607)
    sleep(rnd(1000,2000))
    
    XM.RndTap(630,515)
    sleep(rnd(3000,5000))
    --    waitPic(572,167,639,208,6,2,1)
    if waitPic(572,167,639,208,6,2,1)==true then
        while waitPic(572,167,639,208,120,30)==true do
            XM.Print("排队等待中")
        end
    end
    if waitPic(572,167,639,208,6,10,5)==true then
        
    end
end
ROLE_TYPE={
{146,137,903,431},
{146,137,1011,432},
{146,137,1101,431},
{146,137,906,488},
{140,361,903,431},
{139,444,1101,431}

}
function getName()
    local p1=math.floor(name_idx/10)
    local tp=name_tempale[p1+1]
    local tp1=rnd(10,90)+p1%10
    role_name=tp..tostring(tp1)
    name_idx=name_idx+1
    return role_name
end
function create_user(zy)
    XM.Print(zy)
    local p=ROLE_TYPE[zy]
    XM.RndTap(p[1],p[2])
    sleep(rnd(2000,3000))
    XM.RndTap(p[3],p[4])
    sleep(rnd(2000,3000))
    local username=getName()
    XM.RndTap(999,576)
    sleep(rnd(2000,3000))
    inputtext(username)
    sleep(rnd(300,600))
    XM.RndTap(1244,650)
    sleep(rnd(2000,3000))
    XM.RndTap(1009,651)
    sleep(rnd(3000,5000))
    while waitColor("角色创建",false,120,1)==true do
        RquitApp()
    end
end
function RquitApp()
    XM.Print("quick app")
    syskillapp("com.hegu.dnl.sn79")
    sleep(5000)
end
function doSkipFlow()
    -- 建角色流程
    quickSkip()
    
end
H["角色创建"]={
{"角色创建",0.9,145,22,155,36,"15243B-111111","1|4|F2EDC0-111111,1|6|14233A-111111"},
{"开始新手",0.9,1066,34,1082,52,"0F111E-111111","2|6|F1C057-111111,4|9|3D232A-111111"}
}
function RcreateUserFull()
    XM.RndTap(1105,663)
    XM.SetTableID("角色创建")
    if  waitColor("角色创建",false,10,1) then
        XM.Print("进入角色创建页")
        local role_type=rnd(1,6)
        XM.Print("创建角色类型"..role_type)
        create_user(role_type)
        return true
    end
    return false
    
end
function quickSkip()
    for i=0,5,1 do
        XM.RndTap(1132,49)
        sleep(200)
    end
end