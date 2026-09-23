import type { RefObject } from 'react'

// Stylized outline traced from the supplied visual reference, not geographic data.
const outline = 'M32 305 36 292 34 284 39 275 43 274 45 264 51 263 56 274 62 276 63 260 71 255 73 250 83 245 90 237 97 240 103 237 105 241 115 241 120 237 128 239 132 245 141 250 144 260 147 254 153 258 159 260 165 254 165 251 171 252 175 249 179 252 183 249 190 252 196 248 201 256 212 260 217 255 224 259 232 257 237 254 239 245 233 242 224 241 225 237 218 234 223 229 231 226 231 220 227 216 233 211 246 209 239 205 232 204 236 200 231 197 234 189 239 191 249 188 257 189 269 185 289 181 290 177 308 173 320 172 329 168 332 164 340 164 342 159 352 164 359 164 365 168 369 164 374 168 373 175 379 178 376 183 384 188 389 183 395 189 401 189 407 189 404 194 403 197 409 196 414 199 421 193 430 190 433 186 443 184 450 181 453 183 450 187 446 189 457 198 466 209 476 225 494 254 499 253 500 246 506 246 511 253 516 256 528 256 538 251 545 253 551 259 554 268 562 270 567 280 576 281 581 279 586 277 589 284 595 287 592 292 588 292 588 301 580 305 575 306 572 313 572 324 573 331 566 337 560 334 553 335 543 333 538 331 530 355 526 366 530 369 529 373 525 374 520 370 509 373 495 378 501 382 504 405 505 414 499 418 502 422 498 426 498 433 490 428 485 423 472 420 453 419 449 422 439 420 434 422 425 419 418 414 410 415 405 420 404 430 392 425 381 422 372 424 369 432 362 439 358 438 352 445 345 450 338 458 336 467 330 464 329 458 322 455 309 454 308 442 302 438 302 426 300 420 297 420 295 410 289 403 280 406 262 405 249 408 244 405 231 387 199 365 164 376 164 451 158 454 152 449 145 437 137 432 129 432 121 437 114 443 114 434 117 425 111 421 106 421 104 415 99 414 97 404 91 397 90 392 85 390 84 384 91 384 96 386 98 382 93 378 99 370 110 368 117 361 122 353 121 342 124 339 118 336 113 338 108 338 99 334 87 340 75 345 69 350 61 346 60 341 65 339 61 332 59 327 54 323 51 319 45 321 44 317 35 316 36 309Z'

export function KazakhstanMap({ sceneRef }: { sceneRef: RefObject<SVGGElement | null> }) {
  return <svg className="kazakhstan-map" aria-hidden="true">
    <defs>
      <path id="kz-outline" d={outline}/>
      <pattern id="map-dots" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".7" fill="#96c68b" opacity=".35"/></pattern>
      <linearGradient id="map-fill" x2=".8" y2="1"><stop stopColor="#315d40" stopOpacity=".65"/><stop offset="1" stopColor="#152e23" stopOpacity=".5"/></linearGradient>
      <linearGradient id="map-sweep"><stop stopColor="#b8e797" stopOpacity="0"/><stop offset=".5" stopColor="#b8e797" stopOpacity=".13"/><stop offset="1" stopColor="#b8e797" stopOpacity="0"/></linearGradient>
      <clipPath id="map-clip"><use href="#kz-outline"/></clipPath>
    </defs>
    <g ref={sceneRef}><g transform="translate(-5 -98) scale(1.3)"><g className="map-drift">
      <use href="#kz-outline" transform="translate(0 7)" fill="#06110c" stroke="#416348" strokeOpacity=".25"/>
      <use href="#kz-outline" fill="url(#map-fill)" stroke="#91bd83" strokeOpacity=".65" strokeWidth="1"/>
      <use href="#kz-outline" fill="url(#map-dots)"/>
      <g clipPath="url(#map-clip)"><rect className="map-sweep" x="-150" y="140" width="160" height="340" fill="url(#map-sweep)"/></g>
      <text x="325" y="357" textAnchor="middle" fill="#b0ccaa" opacity=".35" fontSize="10" letterSpacing="8">QAZAQSTAN</text>
    </g></g></g>
  </svg>
}
