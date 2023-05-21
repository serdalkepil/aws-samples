using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TravelBuddy.Models
{
    public class FlightSpecial
    {
        public String header { get; set; }
        public String body { get; set; }
        public int cost { get; set; }
        public long expiryDate { get; set; }
        public String origin { get; set; }
        public String originCode { get; set; }
        public String destination { get; set; }
        public String destinationCode { get; set; }
    }
}