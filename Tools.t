function toolsFunc()
    XM.Print("tools function")
end

function get_text(x1,y1,x2,y2,colors)
    local ret=cmd("su root screencap -p /sdcard/01.png")
    local url=string.format("%s/upload?x1=%s&y1=%s&x2=%s&y2=%s&colors=%s",SERVER_ADDR,x1,y1,x2,y2,colors)
    
    local command_str=string.format("curl -F \"ocr_file=@/sdcard/01.png\" \"%s\"",url)
    XM.Print("执行str："..command_str)
    ret=cmd(command_str)
    --    cmd("rm /sdcard/01.png")
    XM.Print("url请求结果"..ret)
end
function compare_img(x1,y1,x2,y2,target)
    local ret=cmdnew("su root screencap -p /sdcard/01.png")
    local url=string.format("%s/compare_img?x1=%s&y1=%s&x2=%s&y2=%s&target=%s",
    SERVER_ADDR,x1,y1,x2,y2,target)
    
    local command_str=string.format("curl --connect-timeout 10 -F \"ocr_file=@/sdcard/01.png\" \"%s\"",url)
    XM.Print("执行str："..command_str)
    ret=cmdnew(command_str)
    --    cmd("rm /sdcard/01.png")
    return ret=="True"
end
function waitColor(id,click,timeout,step)
    if timeout==nil then
        timeout=5
    end
    if click==nil then
        click=false
        
    end
    if step==nil then
        step=1
    end
    XM.Print(tostring(click))
    return waitFound(timeout,step,(function ()
    keepcapture(0)
    XM.Print(tostring(id))
    XM.Print(tostring(click))
    local ret= XM.Find(5,id,click)
    releasecapture(0)
    return ret
    end))
end
function waitPic(x1,y1,x2,y2,id,timeout,step)
    if timeout==nil then
        timeout=120
    end
    if step==nil then 
        step=10
    end
    return waitFound(timeout,step,(function ()
    return compare_img(x1,y1,x2,y2,id)
    end))
end
