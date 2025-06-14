/**  
当使用Ai算子进行推理时，同一个模型若标注了多类标签，为了便于将不同标签进行分类，故编写了本算子
该版本需要加入一个标签的stringarray数组，使得输出的二维数组行能够根据输入的names的顺序进行排列

使用方法：
将Ai算子一个模型的"输出目标类别名（stringarray）"连接至本函数的type输入，并创建一个stringarray的数组，强中包含期望排序的标签名称，
函数将会输出一个二维数组，数组的每一行是一个类别，行的顺序根据names的数组顺序对应，每一个元素是对应的Ai输出的各类数据数组的位置。
如：type={b,a,c,c,a,d} names={a,b,c} result={{1,4},{0},{2,3}}
程序赋值为：
result.ArrayDeepCopy(AITargetClassification(type，names).Value);
//20250322tio

*/ 
 

function AITargetClassificationBynames(type, names){ 
    // 创建一个对象来存储分类结果
    var classification = {};
    var TargetClassification = IntegerArrayArray(); // 创建二维数组

    for (var i = 0; i < type._Size(); i++) {
        var name = type._At(i).Value; // 获取当前名称

        // 如果该名称尚未在分类对象中，则初始化一个数组
        if (!classification[name]) {
            classification[name] = [];
        }

        // 将当前索引添加到对应名称的数组中
        classification[name].push(i); // 记录索引
    }

    // 调试输出分类结果
    //Log.writeDebug("Classification Result: " + JSON.stringify(classification));

    // 遍历 names 数组并根据顺序推入 TargetClassification
    for (var j = 0; j < names._Size(); j++) {
        var nameKey = names._At(j).Value; // 获取当前名称
        if (classification[nameKey]) {
            var oneDimensionalArray = IntegerArray(); // 创建一维数组
            for (var k = 0; k < classification[nameKey].length; k++) {
                oneDimensionalArray._Push_Back(Integer(classification[nameKey][k])); // 将索引推入一维数组
            }
            TargetClassification._Push_Back(oneDimensionalArray); // 将一维数组推入 TargetClassification
        }
    }

    // 调试输出最终结果
    //Log.writeDebug("Final Target Classification: " + JSON.stringify(TargetClassification));

    return TargetClassification; // 返回最终的二维数组
}