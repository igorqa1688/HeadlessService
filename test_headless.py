import headless_service_pb2_grpc
import headless_service_pb2
from functions import grpc_channel, generate_guid, generate_random_balance
from requests import add_or_update_headless, get_headless_by_one_param


# Только club_guid
def test_add_or_update_headless_club_guid(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    club_guid = generate_guid()
    nous_account_guid =generate_guid()
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert response.chips_balance == 0
    assert response.room_player_guid == ""
    assert response.club_guid == club_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == 0


# Только chips_balance
def test_add_or_update_headless_chips_balance(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    chips_balance = 1
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == ""
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == 0


# Только gold_balance
def test_add_or_update_headless_gold_balance(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    gold_balance = 1
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        gold_balance=gold_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == 0
    assert response.room_player_guid == ""
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == 1


# Только room_player_guid
def test_add_or_update_headless_room_player_guid(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    room_player_guid = generate_guid()
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        room_player_guid=room_player_guid,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == 0
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == 0


# Заполнены все поля
def test_add_or_update_headless_full_data(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 10000
    chips_balance = 10001
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# chips_balance меньше 0
def test_add_or_update_headless_chips_balance_less_zero(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 1000
    chips_balance = -1
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# gold_balance меньше 0
def test_add_or_update_headless_gold_balance_less_zero(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid =generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = -100
    chips_balance = 1
    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)

    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# Получение двух headlesses клуба
def test_get_club_headlesses(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    headlesses_count = 2
    club_guid = generate_guid()

    for i in range(headlesses_count):
        room_player_guid = generate_guid()
        gold_balance = generate_random_balance(1, 50)
        chips_balance = generate_random_balance(100, 1000)
        created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
        request = headless_service_pb2.GetClubHeadlessesRequest(club_guid=created_headless.club_guid)
        response = stub.GetClubHeadlesses(request)

        assert len(response.headlesses[i].guid) == 36
        assert response.headlesses[i].club_guid == club_guid
        assert response.headlesses[i].room_player_guid == room_player_guid
        assert response.headlesses[i].gold_balance == gold_balance
        assert response.headlesses[i].chips_balance == chips_balance


# Получение одного headless клуба
def test_get_club_headlesses_one(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    club_guid = generate_guid()
    room_player_guid = generate_guid()
    gold_balance = generate_random_balance(1, 50)
    chips_balance = generate_random_balance(100, 1000)
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
    request = headless_service_pb2.GetClubHeadlessesRequest(club_guid=created_headless.club_guid)
    response = stub.GetClubHeadlesses(request)

    for i in range(len(response.headlesses)):
        assert len(response.headlesses[i].guid) == 36
        assert response.headlesses[i].club_guid == club_guid
        assert response.headlesses[i].room_player_guid == room_player_guid
        assert response.headlesses[i].gold_balance == gold_balance
        assert response.headlesses[i].chips_balance == chips_balance


# Получение одного headless клуба
def test_get_headless(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    club_guid = generate_guid()
    room_player_guid = generate_guid()
    gold_balance = generate_random_balance(1, 50)
    chips_balance = generate_random_balance(100, 1000)

    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
    request = headless_service_pb2.GetHeadlessRequest(nous_account_guid=created_headless.nous_account_guid,
                                                      room_player_guid=created_headless.room_player_guid)
    response = stub.GetHeadless(request)

    assert len(response.guid) == 36
    assert response.club_guid == club_guid
    assert response.room_player_guid == room_player_guid
    assert response.gold_balance == gold_balance
    assert response.chips_balance == chips_balance


# Изменен chips_balance
def test_update_headless_chips_balance(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 10000
    chips_balance = 10001
    new_chips_balance = generate_random_balance(50,60)
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=new_chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == new_chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# Изменен chips_balance на отрицательное значение
def test_update_headless_chips_balance_less_zero(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 10000
    chips_balance = 10001
    new_chips_balance = -2
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=new_chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == new_chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# Изменен gold_balance
def test_update_headless_gold_balance(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    new_gold_balance = generate_random_balance(50,60)
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=new_gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == new_gold_balance


# Изменен gold_balance на отрицательное значение
def test_update_headless_less_zero_gold_balance(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    new_gold_balance = -1
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=new_gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == new_gold_balance


# Изменен room_player_guid
def test_update_headless_room_player_guid(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    new_room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=new_room_player_guid,
        gold_balance=gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == new_room_player_guid
    assert response.nous_account_guid == nous_account_guid
    assert response.gold_balance == gold_balance


# Изменен nous_account_guid
def test_update_headless_room_player_guid(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    new_nous_account_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=club_guid,
        room_player_guid=room_player_guid,
        gold_balance=gold_balance,
        chips_balance=chips_balance,
        nous_account_guid=new_nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == chips_balance
    assert response.room_player_guid == room_player_guid
    assert response.nous_account_guid == new_nous_account_guid
    assert response.gold_balance == gold_balance


# Изменены все параметры
def test_update_headless_room_edit_all(grpc_channel):
    stub = headless_service_pb2_grpc.HeadlessServiceStub(grpc_channel)
    new_nous_account_guid = generate_guid()
    room_player_guid = generate_guid()
    new_room_player_guid = generate_guid()
    club_guid = generate_guid()
    new_club_guid = generate_guid()
    gold_balance = 40
    new_gold_balance = 5
    chips_balance = 10001
    new_chips_balance = 995

    # Создание headless для редактирования
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)

    request = headless_service_pb2.AddOrUpdateHeadlessRequest(
        club_guid=new_club_guid,
        room_player_guid=new_room_player_guid,
        gold_balance=new_gold_balance,
        chips_balance=new_chips_balance,
        nous_account_guid=new_nous_account_guid)

    response = stub.AddOrUpdateHeadless(request)
    assert len(response.guid) == 36
    assert response.chips_balance == new_chips_balance
    assert response.room_player_guid == new_room_player_guid
    assert response.nous_account_guid == new_nous_account_guid
    assert response.gold_balance == new_gold_balance


# Получение headless по nous_account_guid
def test_get_headless_by_nous_account_guid() -> None:
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    # Создание headless
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
    nous_account_guid = created_headless.nous_account_guid
    get_headless_by_nous_account_guid = get_headless_by_one_param(nous_account_guid, None, None)
    assert len(get_headless_by_nous_account_guid.guid) == 36
    assert get_headless_by_nous_account_guid.nous_account_guid == created_headless.nous_account_guid
    assert get_headless_by_nous_account_guid.room_player_guid == room_player_guid
    assert get_headless_by_nous_account_guid.club_guid == club_guid
    assert get_headless_by_nous_account_guid.chips_balance == chips_balance
    assert get_headless_by_nous_account_guid.gold_balance == gold_balance


# Получение headless по room_player_guid
def test_get_headless_by_room_player_guid() -> None:
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    # Создание headless
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
    nous_account_guid = created_headless.nous_account_guid
    get_headless_by_room_player_guid = get_headless_by_one_param(nous_account_guid, None, None)
    assert len(get_headless_by_room_player_guid.guid) == 36
    assert get_headless_by_room_player_guid.nous_account_guid == created_headless.nous_account_guid
    assert get_headless_by_room_player_guid.room_player_guid == room_player_guid
    assert get_headless_by_room_player_guid.club_guid == club_guid
    assert get_headless_by_room_player_guid.chips_balance == chips_balance
    assert get_headless_by_room_player_guid.gold_balance == gold_balance


# Получение headless по club_guid
def test_get_headless_by_club_guid() -> None:
    room_player_guid = generate_guid()
    club_guid = generate_guid()
    gold_balance = 40
    chips_balance = 10001
    # Создание headless
    created_headless = add_or_update_headless(club_guid, room_player_guid, gold_balance, chips_balance)
    nous_account_guid = created_headless.nous_account_guid
    get_headless_by_club_guid = get_headless_by_one_param(nous_account_guid, None, None)
    assert len(get_headless_by_club_guid.guid) == 36
    assert get_headless_by_club_guid.nous_account_guid == created_headless.nous_account_guid
    assert get_headless_by_club_guid.room_player_guid == room_player_guid
    assert get_headless_by_club_guid.club_guid == club_guid
    assert get_headless_by_club_guid.chips_balance == chips_balance
    assert get_headless_by_club_guid.gold_balance == gold_balance


# Получение headless по несуществующему nous_account_guid
def test_get_headless_by_no_exist_nous_account_guid() -> None:
    result = get_headless_by_one_param(generate_guid(), None, None)
    # Распаковка ответа
    status_code = result.code()
    grpc_details = result.details()
    assert status_code.value[0] == 5
    assert grpc_details == "No headless"


# Получение headless по несуществующему room_player_guid
def test_get_headless_by_no_exist_room_player_guid() -> None:
    result = get_headless_by_one_param(None, generate_guid(), None)
    # Распаковка ответа
    status_code = result.code()
    grpc_details = result.details()
    assert status_code.value[0] == 5
    assert grpc_details == "No headless"


# Получение headless по несуществующему club_guid
def test_get_headless_by_no_exist_club_guid() -> None:
    result = get_headless_by_one_param(None, None, generate_guid())
    # Распаковка ответа
    status_code = result.code()
    grpc_details = result.details()
    assert status_code.value[0] == 5
    assert grpc_details == "No headless"
