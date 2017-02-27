using MarketClient.DataEntries;
using MarketClient.Utils;

namespace MarketClient
{
    public interface IMarketClient
    {
        /// <summary>
        /// Send a buy request to the market server
        /// </summary>
        /// <param name="price">price for the item</param>
        /// <param name="commodity">id of the item</param>
        /// <param name="amount">amount to buy</param>
        /// <returns>the buy request id</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        int SendBuyRequest(int price, int commodity, int amount);

        /// <summary>
        /// Send a sell request to the market server
        /// </summary>
        /// <param name="price">price for the item</param>
        /// <param name="commodity">id of the item</param>
        /// <param name="amount">amount to sell</param>
        /// <returns>the sell request id</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        int SendSellRequest(int price, int commodity, int amount);

        /// <summary>
        /// Query the server about a sell/buy request.
        /// </summary>
        /// <param name="id">id of the request</param>
        /// <returns>data about that request.</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        MarketItemQuery SendQueryBuySellRequest(int id);

        /// <summary>
        /// Query the server about the market state of a the login user.
        /// </summary>
        /// <returns>data about the state of the user</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        MarketUserData SendQueryUserRequest();

        /// <summary>
        /// Query the server about an item.
        /// </summary>
        /// <param name="commodity">id of the item</param>
        /// <returns>the highest bid and the lowest price for this item</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        MarketCommodityOffer SendQueryMarketRequest(int commodity);

        /// <summary>
        /// Cancel a buy/sell request.
        /// </summary>
        /// <param name="id">id of the request</param>
        /// <returns>true iff the request got canceled or error otherwise</returns>
        /// <exception cref="MarketException">error is throw in case of invalid request or invalid parameter.</exception>
        bool SendCancelBuySellRequest(int id);

    }
}
