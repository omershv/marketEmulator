using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using MarketClient.DataEntries;
using Newtonsoft.Json;

namespace MarketClientTest
{
    [TestClass]
    public class JsonTest
    {
        [TestMethod]
        public void TestJsonParserMarketCommodityOffer()
        {
            var marketCommodityOffer = JsonConvert.DeserializeObject<MarketCommodityOffer>("{\"ask\": 5, \"bid\": 10}");
            Assert.IsNotNull(marketCommodityOffer);
            Assert.AreEqual(marketCommodityOffer.Ask, 5);
            Assert.AreEqual(marketCommodityOffer.Bid, 10);
        }

        [TestMethod]
        public void TestJsonParserMarketItemQuery()
        {
            var marketItemQuery =
                JsonConvert.DeserializeObject<MarketItemQuery>(
                    "{\"price\": 5, \"amount\": 10, \"type\": \"sell\", \"user\": \"user99\", \"commodity\": 1}");
            Assert.IsNotNull(marketItemQuery);
            Assert.AreEqual(marketItemQuery.Type, MarketItemQuery.MarketType.Sell);
            Assert.AreEqual(marketItemQuery.Price, 5);
            Assert.AreEqual(marketItemQuery.Amount, 10);
            Assert.AreEqual(marketItemQuery.User, "user99");
            Assert.AreEqual(marketItemQuery.Commodity, 1);
        }


        [TestMethod]
        public void TestJsonParserMarketUserData()
        {
            var marketUserData =
                JsonConvert.DeserializeObject<MarketUserData>(
                    "{\"commodities\": {\"0\": 0, \"1\": 0, \"2\": 0, \"3\": 0}, \"funds\": 40, \"requests\": [1, 2]}");
            Assert.IsNotNull(marketUserData);
            var dict = new Dictionary<string, int>() { { "0", 0 }, { "1", 0 }, { "2", 0 }, { "3", 0 } };
            CollectionAssert.AreEquivalent(marketUserData.Commodities, dict);
            Assert.AreEqual(marketUserData.Funds, 40);
            CollectionAssert.AreEquivalent(marketUserData.Requests, new List<int>() { 1, 2 });
        }
        
    }
}
