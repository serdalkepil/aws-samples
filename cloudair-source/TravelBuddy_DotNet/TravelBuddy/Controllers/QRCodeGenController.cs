using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Web.Mvc;
using ZXing;
using ZXing.QrCode;
using ZXing.QrCode.Internal;
using System.Web.Http;
using System.Drawing;
using System.Drawing.Imaging;

namespace TravelBuddy.Controllers
{
    public class QRCodeGenController : Controller
    {
        readonly static BarcodeWriter qrCodeWriter;

        static QRCodeGenController()
        {
            qrCodeWriter = new BarcodeWriter
            {
                Format = BarcodeFormat.QR_CODE,
                Options = new QrCodeEncodingOptions
                {
                    Margin = 1,
                    Height = 500,
                    Width = 500,
                    ErrorCorrection = ErrorCorrectionLevel.Q,
                },
            };
        }

        [System.Web.Mvc.Route("~/qrcodegenerator/{size?}/{text?}")]
        public ActionResult Generate(int size = 500, string text = "TravelBuddy")
        {
            qrCodeWriter.Options.Width = size;
            qrCodeWriter.Options.Height = size;

            var result = new Bitmap(qrCodeWriter.Write(text.Trim()));
            var memoryStream = new MemoryStream();
            result.Save(memoryStream, ImageFormat.Jpeg);
            return File(memoryStream.ToArray(), "image/png");            
        }
    }
}