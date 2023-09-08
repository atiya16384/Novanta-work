
using IronPython.Hosting;
using IronPython.Modules;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace Programs{
public class ObjNumbers{
    public int InitialVal{get; set;}
    public int FirstVal{get; set;}
    public int SecondVal{get;set;}
    public int ThirdVal{get; set;}

}
class Work{
    static void Main(string[] args){

        Console.WriteLine("Execute python IronPython...");
            Option1_IronPython();
        Console.WriteLine();
    }
       //using ironpython
        static void Option1_IronPython(){
            //Create python engine
            var engine = Python.CreateEngine();
            // Provide script and arguments
            var script="C:\\Users\\atiya.mahboob\\Documents\\task4\\pythonCode\\calculate.py";
            var source = engine.CreateScriptSourceFromFile(script);

            // we create an instance of objnumbers class
            // we want to pass an object to the external python script 
        
            // ObjNumbers argv = new()
            // {
            //     InitialVal = 0,
            //     FirstVal = 10,
            //     SecondVal = 20,
            //     ThirdVal = 8,
            // };
            // // 'objNumbers' object is not subscriptable
            List<int> argv = new List<int>
            {
                1,
                2,
                3,
                4,
                5,
            };

            engine.GetSysModule().SetVariable("argv", argv);
            // Output redirect
            var eIO = engine.Runtime.IO;
            var errors = new MemoryStream();
            eIO.SetErrorOutput(errors, Encoding.Default);
            var results = new MemoryStream();
            eIO.SetOutput(results, Encoding.Default);
            //  Execute script 
            var scope = engine.CreateScope();
            source.Execute(scope);
            // Display output
            //index out of bounds error here 
            string str(byte[] x) => Encoding.Default.GetString(x);
            Console.WriteLine("ERRORS:");
            Console.WriteLine(str(errors.ToArray()));
            Console.WriteLine();
            Console.WriteLine("Results:");
            Console.WriteLine(str(results.ToArray()));
    }
}
}