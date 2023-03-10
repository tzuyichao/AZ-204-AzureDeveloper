using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.AzureAppConfiguration;

public static class Demo
{
    static void Main(string[] args) 
    {
        var builder = new ConfigurationBuilder();
        builder.AddAzureAppConfiguration(options => {
            options
                .Connect(Environment.GetEnvironmentVariable("ConnectionString"))
                .Select(KeyFilter.Any, "lab");
        });

        var config = builder.Build();
        Console.WriteLine(config["TestApp:Settings:Message"] ?? "Hello World!");
    }
}