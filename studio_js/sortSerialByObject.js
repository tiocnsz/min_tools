/**   
使用方法为： 
var rr=sortSerialByObject(serial, object,order); 
outarr.ArrayDeepCopy(rr.Value); 
 
serial为数据标号（real或int数组），object为比对数据（real或int数组），order=0降序，order=1升序； 
return值为数据类型与serial相同，根据object对serial进行排序 
后续可根据return数组遍历object得到排序后的数组 
//250121tio 
 
 */  
  

function sortSerialByObject(serial, object,order){ 
     
    if(arguments.length == 3) { //检查是否符合输入  
        if(Object.prototype.toString.call(arguments[0]) == '[object Object]') {  
            var typeName1 = arguments[0].TypeName();  
            var typeName2 = arguments[1].TypeName();  
            if((typeName1 == 'RealArray' || typeName1 == 'IntegerArray')&&(typeName2 == 'RealArray' || typeName2 == 'IntegerArray')){  
 
                var jsAryserial = new Array();   
                var jsAryobject = new Array();                   
                for(var i = 0 ; i < serial._Size(); i++){  
                    jsAryserial.push(serial._At(i).Value);  
                    jsAryobject.push(object._At(i).Value);  
                     
                }  
 
 
 
 
                  // 定义比较函数 
                var compare = function(a, b) { 
                    if (order.Value == 0) { // 降序 
                        return jsAryobject[b] - jsAryobject[a]; 
                         
                    } else if (order.Value == 1) { // 升序 
                        return jsAryobject[a] - jsAryobject[b]; 
                    } else { 
                        throw new Error('Invalid order parameter. Use "0" for descending or "1" for ascending.'); 
                    } 
                }; 
 
                //定义排序序号数组 
                var sortedIndices = new Array(); 
                for (var i = 0; i < jsAryserial.length; i++) { 
                    sortedIndices.push(i); 
                } 
                 //冒泡算法对索引排序 
                 for (var i = 0; i < sortedIndices.length - 1; i++) { 
                        for (var j = 0; j < sortedIndices.length - 1 - i; j++) { 
                            if (compare(sortedIndices[j], sortedIndices[j + 1]) > 0) { 
                        // 交换索引 
                                var r1=sortedIndices[j]; 
                                var r2=sortedIndices[j+1];           
                                sortedIndices[j + 1]=r1; 
                                sortedIndices[j ]=r2; 
                            } 
                          } 
                    } 
 
                     
                     
                var aryserialCpy;  
                if(typeName1 == 'RealArray'){  
                    aryserialCpy = RealArray();  
                } else {  
                    aryserialCpy = IntegerArray();  
                }  
                    
 
 
 
                //将组合的进行拆分只取根据jsAryobject排序后的jsAryserial并构建循环构建新数组 
 
                for(var i = 0 ; i < sortedIndices.length; i++){  
 
                    aryserialCpy._Push_Back(Integer(jsAryserial[sortedIndices[i]])); 
                     
               }  
                 
 
               return aryserialCpy;  
            }  
            else {  
               throw new Error('Parameter mismatch: ' + 'wrong type or wrong param number!');  
            }  
        }  
    }  
} 
