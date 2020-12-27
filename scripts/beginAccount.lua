-- 自动启动游戏，创建账号，然后启动紫龙脚本，起号
Unit.Param.beginAccount={

}

function Unit.State.beginAccount(taskInfo)
    if taskInfo.from=="createRole" then
        return "loginAccount"
    end
    if taskInfo.from=="loginAccount" then
        return "startZL"
    end
    
    if taskInfo.from=="startZL" then
        if  startSS() then
            return "waitZLok"
        end
    end
    
    return "createRole"
    -- return "loginAccount"
    -- if taskInfo.task=="内置账号" then
    --     -- toast(text,time)
    --     Unit.Param.createRole={
    --         task="beginAccount"
    --     }
    --     return "createRole"
    -- end
    
end
Unit.Param.waitZLok={
   
}

function Unit.State.waitZLok(param) 
    nLog("等待紫龙脚本退出")
    while appIsRunning ("com.aland.hsz")==1 do 
        mSleep(60*1000*60)
    end
    return "beginAccount"
    
end

Unit.Param.startZL={

}

function Unit.State.startZL(param)
    init(0)
    os.execute("input keyevent KEYCODE_HOME")
        
    closeApp("com.aland.hsz")
    mSleep(2000)
    tap(947,621)
    tap(111,597)
    mSleep(20000)
    nLog("等待紫龙")
    tap(625,337)
    mSleep(2000)
    tap(373,1233)
    mSleep(2000)
    tap(432,1090)
    mSleep(2000)

    init(1)
    return param.from
    -- Unit.Param.Error.errorType="beginAccount"
    -- Unit.Param.Error.name="beginAccount"
    -- return "Error"
end
