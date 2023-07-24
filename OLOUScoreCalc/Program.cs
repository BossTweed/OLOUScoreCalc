using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using System.Text;
using IOF.XML.V3;
using System.Xml.Serialization;
using System.IO;

namespace OLOUScoreCalc;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        var serviceProvider = new ServiceCollection()
        .AddLogging()
        .AddSingleton<IXmlSerializerService, XmlSerializerService>()
        .BuildServiceProvider();

        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

        var _XmlSerializerService = serviceProvider.GetService<IXmlSerializerService>();

        var xmlInputFilePath = @"C:\Users\Justin\source\testdata\results\results-IOFv3.xml";
        var xmlOutputFilePath = @"C:\Users\Justin\source\testdata\results\resultsOut-IOFv3.xml";


        var results = _XmlSerializerService.Deserialize<ResultList>(xmlInputFilePath);

        _XmlSerializerService.Serialize<ResultList>(xmlOutputFilePath, results);

    }
}


public interface IXmlSerializerService
{
    T Deserialize<T>(string path) where T : class;
    void Serialize<T>(string path, T instance);
}

public class XmlSerializerService : IXmlSerializerService
{
    public XmlSerializerService()
    {
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
    }

    public void Serialize<T>(string path, T instance)
    {
        using(FileStream fileStream = new FileStream(path, FileMode.Create))
        {
            new XmlSerializer(typeof(T)).Serialize(fileStream, instance);
        }
    }

    public T Deserialize<T>(string path)where T : class
    {
        if (!File.Exists(path))
        {
            return null;
        }

        using(FileStream fileStream = new FileStream(path, FileMode.Open))
        {
            return new XmlSerializer(typeof(T)).Deserialize(fileStream)as T;
        }
    }
}