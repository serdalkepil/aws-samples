using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TravelBuddy.Models
{
    public class FlightHotelModel
    {
        public List<FlightSpecial> flightSpecials { get; set; }
        public List<HotelSpecial> hotelSpecials { get; set; }
        public string errorMessage { get; set; }
        public bool isErrorOnPage { get; set; }
        
        public FlightHotelModel(
            List<FlightSpecial> flightSpecials,
            List<HotelSpecial> hotelSpecials,
            bool isErrorOnPage,
            string errorMessage
            )
        {
            this.flightSpecials = flightSpecials;
            this.hotelSpecials  = hotelSpecials;
            this.isErrorOnPage  = isErrorOnPage;
            this.errorMessage   = errorMessage;
        }
    }
}