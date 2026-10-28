void CalculateLuggageFee()
{
    float weight, overWeight;
    int cabinClass;      // 1=头等舱 2=公务舱 3=经济舱
    int passengerType;   // 1=正常 2=外国 3=残疾
    float baseRate = 0;
    float discount = 1.0;
    float fee = 0;

    // 输入
    input(weight, cabinClass, passengerType);

    if (weight <= 20)
    {
        fee = 0;
    }
    else
    {
        overWeight = weight - 20;

        // 舱位判断
        if (cabinClass == 1)
            baseRate = 6;
        else if (cabinClass == 2)
            baseRate = 8;
        else if (cabinClass == 3)
            baseRate = 10;

        // 乘客类型判断
        if (passengerType == 2)
            discount = 2.5;      // 外国乘客
        else if (passengerType == 3)
            discount = 0.5;      // 残疾乘客
        else
            discount = 1.0;

        fee = overWeight * baseRate * discount;
    }

    output(fee);
}