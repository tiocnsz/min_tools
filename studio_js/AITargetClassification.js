/**  
当使用Ai算子进行推理时，同一个模型若标注了多类标签，为了便于将不同标签进行分类，故编写了本算子


使用方法：
将Ai算子一个模型的“输出目标类别名（stringarray）”连接至本函数的type输入，函数将会输出一个二维数组，数组的每一行是一个类别，每一个元素是对应的Ai输出的各类数据数组的位置。
程序赋值为：
result.ArrayDeepCopy(AITargetClassification(type).Value);
//20250219tio
*/ 

function AITargetClassification(type){ 
    var classification = {};
    var TargetClassification = IntegerArrayArray(); 
   // TargetClassification
   for (var i = 0; i < type._Size(); i++) {
       var name = type._At(i).Value; // 获取当前名称

       // 如果该名称尚未在分类对象中，则初始化一个数组
       if (!classification[name]) {
           classification[name] = [];
       }

       // 将当前名称添加到对应的数组中
        classification[name].push(i); // 记录索引
   }

   // 将分类结果转换为二维数组
   
   var result = []; 
   for (var key in classification) {
       var oneDimensionalArray = IntegerArray(); // 创建一维数组
       for (var j = 0; j < classification[key].length; j++) {
          // Log.writeDebug(classification[key].length);  
           oneDimensionalArray._Push_Back(Integer(classification[key][j]));
       }
       
       //result._Push_Back(oneDimensionalArray.Value); // 将一维数组推入二维数组

       
       TargetClassification._Push_Back(oneDimensionalArray);
       oneDimensionalArray.Clear();
       
   }
   return TargetClassification; // 返回二维数组
   }