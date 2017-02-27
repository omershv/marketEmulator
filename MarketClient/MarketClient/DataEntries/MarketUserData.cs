using System.Collections.Generic;

namespace MarketClient.DataEntries
{
    public class MarketUserData
    {
        public Dictionary<string,int> Commodities { get; set; }
        public int Funds { get; set; }
        public List<int> Requests { get; set; }
    }
}