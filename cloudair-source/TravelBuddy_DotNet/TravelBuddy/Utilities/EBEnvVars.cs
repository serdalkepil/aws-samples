using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Web;

namespace TravelBuddy.Utilities
{
    public class EBEnvVars
    {
        public EBEnvVars()
        {
        }

        public static void Init()
        { 
            Dictionary<string, string> result = new Dictionary<string, string>();

            string ConfigurationFilename = @"C:\Program Files\Amazon\ElasticBeanstalk\config\containerconfiguration";
            
            if (System.IO.File.Exists(ConfigurationFilename))
            {
                string configJson;
                try
                {
                    configJson = System.IO.File.ReadAllText(ConfigurationFilename);
                    var config = JObject.Parse(configJson);

                    var env = (JArray)config["iis"]["env"];

                    foreach (string item in env)
                    {
                        int eqIndex = item.IndexOf('=');
                        ConfigurationManager.AppSettings[item.Substring(0, eqIndex)] = item.Substring(eqIndex + 1);
                    }
                }
                catch
                {
                    // Couldn't read the container details directly - no recovery...       
                }
            }
        }
    }
}