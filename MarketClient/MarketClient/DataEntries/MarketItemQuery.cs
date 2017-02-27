namespace MarketClient.DataEntries
{
    public class MarketItemQuery
    {
        public enum MarketType
        {
            Buy,
            Sell
        }

        public int Price { get; set; }
        public int Amount { get; set; }
        public MarketType Type { get; set; }
        public string User { get; set; }
        public int Commodity { get; set; }
    }
}