// Program.cs
// File Type Report

using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;

namespace FileTypeReport
{
    internal static class Program
    {
        private static IEnumerable<string> EnumerateFilesRecursively(string path)
        {
            // yields files found in path.
            foreach (string file in Directory.GetFiles(path)) yield return file;

            // yields files in directories of path recursively.
            foreach (string dir in Directory.GetDirectories(path))
            {
                foreach (string file in EnumerateFilesRecursively(dir))
                {
                    yield return file;
                }
            }
        }
        private static string FormatByteSize(long byteSize)
        {
            if (byteSize >= 0 && byteSize < 1000)
            {
                // find by BYTE if argument is between 0 and 999.
                return byteSize.ToString() + "B";
            }
            else if (byteSize >= 1000)
            {
                foreach (int i in Enumerable.Range(1, 8))
                {
                    // iterates over each category of bytes.
                    if (byteSize < Math.Pow(10, i * 3))
                    {

                        string b;
                        // match to byte type.
                        switch (i - 1)
                        {
                            case 1:
                                // KB
                                b = "kB";
                                break;

                            case 2:
                                // MB
                                b = "MB";
                                break;

                            case 3:
                                // GB
                                b = "GB";
                                break;

                            case 4:
                                // TB
                                b = "TB";
                                break;

                            case 5:
                                // PB
                                b = "PB";
                                break;

                            case 6:
                                // EB
                                b = "EB";
                                break;

                            default:
                                // ZB
                                b = "ZB";
                                break;

                        }
                        return Math.Round(byteSize / Math.Pow(10, (i - 1) * 3), 2).ToString() + b;
                    }
                }
                // since long can't store numbers at 10^21, it is not possible to demonstrate ZB.
                // If it hypothetically was possible, there would an exception here saying the number is too big
                // to be represented according to the problem's requirements.
                // EX. throw new Exception("Byte size is greater than 1000ZB.");
            }
            // exception if byte is less than 0, or long misrepresents a value.
            throw new Exception("Byte size is either below 0, or above the max value of a 'long' type.");
        }


        private static XDocument CreateReport(IEnumerable<string> files)
        {
            // Create an HTML report file
            var query =
            from file in files
            let fileInfo = new FileInfo(file)
            orderby fileInfo.Length descending
            group fileInfo by fileInfo.Extension.ToLower() into fileGroup
            select new
            {
                Type = fileGroup.Key,
                Count = fileGroup.Count(),
                TotalSize = FormatByteSize(fileGroup.Sum(file => file.Length))
            };

            var alignment = new XAttribute("align", "right");
            var style = "table, th, td { border: 1px solid black; }";

            var tableRows = query.Select(row =>
              new XElement("tr",
              new XElement("td", row.Type),
              new XElement("td", row.Count),
              new XElement("td", row.TotalSize)
              )
          );

            var table = new XElement("table",
            new XElement("thead",
              new XElement("tr",
                  new XElement("th", "Type"),
                  new XElement("th", "Count"),
                  new XElement("th", "Total Size"))),
            new XElement("tbody", tableRows));

            return new XDocument(
            new XDocumentType("html", null, null, null),
                new XElement("html",
                  new XElement("head",
                        new XElement("title", "File Report"),
                        new XElement("style", style)),
                  new XElement("body", table)));
        }

        public static void Main(string[] args)
        {
            /*
		    Take two command line arguments. 
		     first value is the path of the input folder and the second the path (including file name and extension) of the HTML report output file. 
		    */
            try
            {
                string inputFolder = args[0];
                string reportFile  = args[1];
                CreateReport(EnumerateFilesRecursively(inputFolder)).Save(reportFile);
            }
            catch
            {
                Console.WriteLine("Usage: FileTypeReport <folder> <report file>");
            }
        }
    }
}