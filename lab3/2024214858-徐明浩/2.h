void autoDispatchDemand(int elderId, String reqType, String location, boolean isUrgent, boolean isVoice) {
    float priority = 0;
    String matchedWorker = null;
    Order order = null;

    // 1. 紧急判断与预警
    if (isUrgent) {
        triggerAlert(elderId, "紧急求助", location); // 预警推送子女/社区/广播
        priority = 10; // 最高优先级
    }

    // 2. 语音处理
    if (isVoice) {
        String text = voiceRecognition(); // 语音转文本
        reqType = parseReqType(text);     // 解析需求类型
    }

    // 3. 需求类型匹配基准
    if (reqType.equals("维修")) {
        priority += 2;
    } else if (reqType.equals("采购")) {
        priority += 1;
    } else if (reqType.equals("医疗")) {
        priority += 5;
    }

    // 4. 智能供需匹配（位置+空闲+评分）
    matchedWorker = matchNearestService(reqType, location);
    
    // 5. 匹配结果与工单生成
    if (matchedWorker != null) {
        order = createOrder(elderId, reqType, location, priority, matchedWorker);
        dispatchOrder(order); // 派发至服务者、老人、子女端
        updateIntegral(elderId, matchedWorker, reqType); // 积分预统计
    } else {
        manualDispatch(elderId, reqType, location, priority); // 转人工
    }
    
    // 6. 安全监测联动（如燃气/人体感应异常则额外预警）
    if (checkHardwareAlert(elderId)) {
        triggerAlert(elderId, "居家异常", location);
    }
    
    return;
}