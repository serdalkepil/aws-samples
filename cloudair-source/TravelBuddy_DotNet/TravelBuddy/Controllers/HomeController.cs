using MySql.Data.MySqlClient;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Web.Mvc;
using TravelBuddy.Models;

namespace TravelBuddy.Controllers
{
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            List<FlightSpecial> flightSpecials = new List<FlightSpecial>();
            List<HotelSpecial> hotelSpecials = new List<HotelSpecial>();
            bool isErrorOnPage = false;
            string errorMessage = "";
            string constr = "";

            try
            {
                constr = ConfigurationManager.ConnectionStrings["dbConnection"].ConnectionString;
                constr = constr.Replace("DATA_SOURCE", ConfigurationManager.AppSettings["dbDataSource"]);

                using (MySqlConnection con = new MySqlConnection(constr))
                {
                    DateTime now = new DateTime();

                    string queryFlights = "SELECT * from flightspecial where expiryDate > " + now.Ticks + " order by expiryDate";
                    string queryHotels = "SELECT * from hotelspecial  where expiryDate > " + now.Ticks + " order by expiryDate";

                    using (MySqlCommand cmdFlights = new MySqlCommand(queryFlights))
                    {
                        cmdFlights.Connection = con;
                        con.Open();

                        using (MySqlDataReader sdr = cmdFlights.ExecuteReader())
                        {
                            while (sdr.Read())
                            {
                                flightSpecials.Add(new FlightSpecial
                                {
                                    header = sdr["header"].ToString(),
                                    body = sdr["body"].ToString(),
                                    cost = Convert.ToInt32(sdr["cost"]),
                                    destination = sdr["destination"].ToString(),
                                    destinationCode = sdr["destinationCode"].ToString(),
                                    expiryDate = Convert.ToInt64(sdr["expiryDate"]),
                                    origin = sdr["origin"].ToString(),
                                    originCode = sdr["originCode"].ToString()
                                });
                            }
                        }

                        con.Close();
                    }

                    using (MySqlCommand cmdHotels = new MySqlCommand(queryHotels))
                    {
                        cmdHotels.Connection = con;
                        con.Open();

                        using (MySqlDataReader sdr = cmdHotels.ExecuteReader())
                        {
                            while (sdr.Read())
                            {
                                hotelSpecials.Add(new HotelSpecial
                                {
                                    description = sdr["description"].ToString(),
                                    hotel = sdr["hotel"].ToString(),
                                    cost = Convert.ToInt32(sdr["cost"]),
                                    id = Convert.ToInt32(sdr["id"]),
                                    location = sdr["location"].ToString()
                                });
                            }
                        }

                        cmdHotels.Connection = con;

                        con.Close();
                    }
                }
            }        
            catch(Exception ex)
            {
                isErrorOnPage = true;
                errorMessage = ex.Message + " TravelBuddy was trying to connect to host \"" + ConfigurationManager.AppSettings["dbDataSource"] + "\"";
            }
            
            return View(
                new FlightHotelModel(
                    flightSpecials, 
                    hotelSpecials,
                    isErrorOnPage,
                    errorMessage
                    ));
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Contact TravelBuddy for more information!";

            return View();
        }
    }
}