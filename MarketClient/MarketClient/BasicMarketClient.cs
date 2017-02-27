using System.Net.Http;
using MarketClient.DataEntries;
using MarketClient.Utils;
using Newtonsoft.Json;

namespace MarketClient
{
    public class BasicMarketClient : IMarketClient
    {
        private readonly string _marketUrl;
        private readonly string _username;
        private readonly string _token;

        public BasicMarketClient(string marketUrl,string username, string privateKey)
        {
            _marketUrl = marketUrl;
            _username = username;
            _token = RSAHelper.RSASignWithSHA256(username, privateKey);
        }
        public int SendBuyRequest(int price, int commodity, int amount)
        {
            return SendBuySellRequest("buy", price, commodity, amount);
        }

        public int SendSellRequest(int price, int commodity, int amount)
        {
            return SendBuySellRequest("sell", price, commodity, amount);
        }

        private int SendBuySellRequest(string type, int price,int commodity, int amount)
        {
            var json = MarketRequest.CreateBuySellRequest(_username, _token, type, price, commodity, amount);
            var response = SendPostRequest(new StringContent(json));
            int result;
            if(int.TryParse(response,out result))
            {
                return result;
            }
            throw new MarketException(response);
        }

        public MarketItemQuery SendQueryBuySellRequest(int id)
        {
            var json = MarketRequest.CreateQueryBuySellRequest(_username, _token, id);
            var response = SendPostRequest(new StringContent(json));
            return FromJson<MarketItemQuery>(response);
        }


        public MarketUserData SendQueryUserRequest()
        {
            var json = MarketRequest.CreateQueryUserRequest(_username, _token);
            var response = SendPostRequest(new StringContent(json));
            return FromJson<MarketUserData>(response);
        }

        public MarketCommodityOffer SendQueryMarketRequest(int commodity)
        {
            var json = MarketRequest.CreateQueryMarketRequest(_username, _token, commodity);
            var response = SendPostRequest(new StringContent(json));
            return FromJson<MarketCommodityOffer>(response);
        }

        public bool SendCancelBuySellRequest(int id)
        {
            var json = MarketRequest.CreateCancelBuySellRequest(_username, _token, id);
            var response = SendPostRequest(new StringContent(json));
            if (response.Equals("Ok"))
            {
                return true;
            }
            throw new MarketException(response);
        }

        private static T FromJson<T>(string response)
        {
            try
            {
                return JsonConvert.DeserializeObject<T>(response, new JsonSerializerSettings
                {
                    Error = delegate {
                        throw new JsonException(response);
                    }
                });
            }
            catch
            {
                throw new MarketException(response);
            }
        }

        private string SendPostRequest(StringContent content)
        {
            using (HttpClient client = new HttpClient())
            {
                var result = client.PostAsync(_marketUrl, content).Result;
                var responseContent = result.Content.ReadAsStringAsync().Result;
                return responseContent;
            }
        }
    }
}
