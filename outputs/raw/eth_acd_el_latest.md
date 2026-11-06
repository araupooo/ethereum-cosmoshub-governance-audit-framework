# Ethereum Core Devs Meeting #204
### Meeting Date/Time: Jan 30, 2025, 14:00-15:30 UTC
### Meeting Duration: 1 hour 30 mins
### [GitHub Agenda](https://github.com/ethereum/pm/issues/1253)
### [Video of the meeting](https://youtu.be/JW2IWwVKRec)
### Moderator: Tim Bieko
### Notes: Alen (Santhosh)

| Decision Item | Description                                                              | Video ref |
| ------------- | ------------------------------------------------------------------------ | ------------- |
| 204.1 | **Devnet 5 Updates**  A developer by the screen name “pk910” shared updates about Pectra Devnet 5. Though the devnet is finalizing again and the gas estimation bug shared on last week’s ACD call is now resolved among clients, it appears there is a new consensus bug impacting the Nethermind client. Senior software engineer at Nethermind Marek Moraczyński said the bug was caused due to a BLS precompile optimization in the Nethermind client. Moraczyński added that the bug should not be a blocker for the launch of Pectra Devnet 6 as a fix for it has already been implemented by his team.
| 204.2 | **Devnet 6 Updates**  On the topic of Pectra Devnet 6, Pk910 said a new hive release for Pectra is ready. Once most client teams pass the new hive tests, the EF Developer Operations team will launch Pectra Devnet 6. Pk910 said there is a pending change for Devnet 6 specifications impacting system contract addresses. The change will update all system contract addresses created through Pectra to be more recognizable and follow a pattern that highlights which EIP each specific system contract address relates to. Developers agreed to merge these changes on GitHub and finalize them for Devnet 6.
| 204.3 | **Testnet Fork Slot Proposals**  On the prior ACD call, Beiko shared tentative dates for upgrading public Ethereum testnets. Given that developers have not yet launched Pectra Devnet 6, Beiko asked if developers should update their initial timeline and when they would feel comfortable picking more specific ti