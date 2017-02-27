using Newtonsoft.Json;

namespace MarketClient.Utils
{
    /// <summary>
    /// This class will be a factory to create Market requests.
    /// </summary>
    class MarketRequest
    {
       
        public static string CreateBuySellRequest(string user, string token, string type, int price, int commodity, int amount)
        {
            var request = new
            {
                auth = new
                {
                    user, token
                },
                type, price, commodity, amount
            };
            return JsonConvert.SerializeObject(request);
        }

        public static string CreateQueryBuySellRequest(string user, string token, int id)
        {
            var request = new
            {
                auth = new
                {
                    user, token
                },
                type = "queryBuySell", id
            };
            return JsonConvert.SerializeObject(request);
        }

        public static string CreateQueryUserRequest(string user, string token)
        {
            var request = new
            {
                auth = new
                {
                    user, token
                },
                type = "queryUser",
            };
            return JsonConvert.SerializeObject(request);
        }

        public static string CreateQueryMarketRequest(string user, string token, int commodity)
        {
            var request = new
            {
                auth = new
                {
                    user, token
                },
                type = "queryMarket", commodity
            };
            return JsonConvert.SerializeObject(request);
        }

        public static string CreateCancelBuySellRequest(string user, string token, int id)
        {
            var request = new
            {
                auth = new
                {
                    user, token
                },
                type = "cancelBuySell", id
            };
            return JsonConvert.SerializeObject(request);
        }
    }
}
