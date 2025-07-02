# CeneoWebScraper24na25

## Struktura opinii w serwisie Ceneo.pl

| Składowa                               | Zmienna        | Selektor                                                    |
| -------------------------------------- | -------------- | ----------------------------------------------------------- |
| opinia                                 | opinion        | div.js_product-review:not(.user-post--highlight)            |
| identyfikator opinii                   | opinion_id     | ["data-entry-id"]                                           |
| autor                                  | author         | span.user-post\_\_author-name                               |
| rekomendacja                           | recommendation | span.user-post\_\_author-recomendation > em                 |
| liczba gwiazdek                        | stars          | span.user-post\_\_score-count                               |
| treść opinii                           | content        | div.user-post\_\_text                                       |
| lista zalet                            | pros           | div.review-feature\_\_item--positive                        |
| lista wad                              | cons           | div.review-feature\_\_item--negative                        |
| ile osób uznało opinię za przydatną    | useful         | button.vote-yes["data-total-vote"]                          |
| ile osób uznało opinię za nieprzydatną | useless        | button.vote-no["data-total-vote"]                           |
| data wystawienia opinii                | post_date      | span.user-post\_\_published > time:nth-child(1)["datetime"] |
| data zakupu produktu                   | purchase_date  | span.user-post\_\_published > time:nth-child(2)["datetime"] |
