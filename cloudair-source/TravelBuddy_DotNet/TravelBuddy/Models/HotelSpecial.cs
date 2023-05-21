using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TravelBuddy.Models
{
    public class HotelSpecial
    {
        public int id { get; set; }
        public String hotel { get; set; }
        public String description { get; set; }
        public int cost { get; set; }
        public long expiryDate { get; set; }
        public String location { get; set; }
    }
}